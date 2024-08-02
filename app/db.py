from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do URL do banco de dados
DATABASE_URL = "sqlite:///./test.db"

# Criação do engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criação da sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base do modelo
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
