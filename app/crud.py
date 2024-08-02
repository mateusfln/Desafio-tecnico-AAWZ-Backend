from .models import Vendedor
from .db import SessionLocal
from datetime import datetime

class GerenciadorVendedores:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def create_vendedor(self, nome, cpf, data_nascimento, email, estado):
        if self.get_vendedor_by_cpf(cpf):
            raise Exception("CPF Já Cadastrado")
            
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        vendedor = Vendedor(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email,
            estado=estado
        )
        self.db.add(vendedor)
        self.db.commit()
        self.db.refresh(vendedor)
        return vendedor

    def get_vendedor(self, vendedor_id):
        return self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    
    def get_vendedores(self):
        return self.db.query(Vendedor).all()

    def get_vendedor_by_cpf(self, cpf):
        return self.db.query(Vendedor).filter(Vendedor.cpf == cpf).first()

    def update_vendedor(self, vendedor_id, nome=None, cpf=None, data_nascimento=None, email=None, estado=None):
        vendedor = self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        if nome:
            vendedor.nome = nome
        if cpf:
            vendedor.cpf = cpf
        if data_nascimento:
            vendedor.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        if email:
            vendedor.email = email
        if estado:
            vendedor.estado = estado
        self.db.commit()
        self.db.refresh(vendedor)
        return vendedor

    def delete_vendedor(self, vendedor_id):
        vendedor = self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        self.db.delete(vendedor)
        self.db.commit()
        return vendedor
