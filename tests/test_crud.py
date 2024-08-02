import pytest
from app.crud import GerenciadorVendedores
from app.models import Vendedor, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Fixtures do Pytest

@pytest.fixture(scope='module')
def engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope='module')
def session_factory(engine):
    Session = sessionmaker(bind=engine)
    return Session

@pytest.fixture
def session(session_factory):
    session = session_factory()
    yield session
    session.close()

@pytest.fixture
def gerenciador(session):
    return GerenciadorVendedores(db_session=session)

@pytest.fixture
def setup_vendedor(gerenciador, session):
    vendedor = session.query(Vendedor).filter_by(cpf="12345678901").first()
    if vendedor == None:
        vendedor = gerenciador.create_vendedor(
            nome="João",
            cpf="12345678901",
            data_nascimento="1990-01-01",
            email="joao@example.com",
            estado="SP"
        )
        session.commit()
    return vendedor

def test_create_vendedor(gerenciador, session):
    gerenciador.create_vendedor(
        nome="Maria",
        cpf="12345678902",
        data_nascimento="1992-02-02",
        email="maria@example.com",
        estado="RJ"
    )
    fetched_vendedor = session.query(Vendedor).filter_by(cpf="12345678902").first()
    assert fetched_vendedor is not None
    assert fetched_vendedor.nome == "Maria"
    assert fetched_vendedor.email == "maria@example.com"

def test_update_vendedor(gerenciador, session, setup_vendedor):
    vendedor = setup_vendedor  

    gerenciador.update_vendedor(
        vendedor_id=vendedor.id,
        nome="João 2",
        email="joao2@example.com",
        estado="SC"
    )
    fetched_vendedor = session.query(Vendedor).filter_by(cpf="12345678901").first()
    assert fetched_vendedor is not None
    assert fetched_vendedor.nome == "João 2"
    assert fetched_vendedor.email == "joao2@example.com"
    assert fetched_vendedor.estado == "SC"

def test_delete_vendedor(gerenciador, session, setup_vendedor):
    vendedor = setup_vendedor  
    
    gerenciador.delete_vendedor(vendedor.id)
    fetched_vendedor = session.query(Vendedor).filter_by(cpf="12345678901").first()
    assert fetched_vendedor is None

def test_create_vendedor_with_existing_cpf(gerenciador, session, setup_vendedor):
    with pytest.raises(Exception) as excinfo:
        gerenciador.create_vendedor(
            nome="Pedro",
            cpf="12345678901",
            data_nascimento="1995-05-05",
            email="pedro@example.com",
            estado="MG"
        )
    assert "CPF Já Cadastrado" in str(excinfo.value)

def test_get_vendedor(gerenciador, session):
    vendedor = session.query(Vendedor).filter_by(cpf="12345678901").first()
    fetched_vendedor = gerenciador.get_vendedor(vendedor.id)
    assert fetched_vendedor is not None
    assert fetched_vendedor.nome == "João"

def test_get_vendedores(gerenciador):
    vendedores = gerenciador.get_vendedores()
    assert len(vendedores) > 0

def test_get_vendedor_by_cpf(gerenciador):
    vendedor = gerenciador.get_vendedor_by_cpf("12345678901")
    assert vendedor is not None
    assert vendedor.nome == "João"