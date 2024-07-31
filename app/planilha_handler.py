import pandas as pd
from .crud import GerenciadorVendedores

class PlanilhaHandler:
    def __init__(self):
        self.gerenciador = GerenciadorVendedores()

    def importar_vendedores(self, path):
        # Lê a planilha
        df = pd.read_excel(path)

        # Itera sobre as linhas da planilha e adiciona/atualiza os vendedores
        for _, row in df.iterrows():
            try:
                self.gerenciador.create_vendedor(
                    nome=row['nome'],
                    cpf=row['cpf'],
                    data_nascimento=row['data_nascimento'],
                    email=row['email'],
                    estado=row['estado']
                )
            except ValueError:
                # Se o CPF já estiver cadastrado, atualiza o vendedor
                vendedor = self.gerenciador.get_vendedor_by_cpf(row['cpf'])
                self.gerenciador.update_vendedor(
                    vendedor_id=vendedor.id,
                    nome=row['nome'],
                    cpf=row['cpf'],
                    data_nascimento=row['data_nascimento'],
                    email=row['email'],
                    estado=row['estado']
                )

    def calcular_comissoes(self, path):
        df = pd.read_excel(path)
        comissoes = {}
        for _, row in df.iterrows():
            cpf = row['CPF']
            valor_venda = row['Valor Venda']
            canal = row['Canal']

            comissao_vendedor = valor_venda * 0.10
            comissao_marketing = 0
            comissao_gerente = 0

            if canal == 'online':
                comissao_marketing = comissao_vendedor * 0.20
                comissao_vendedor -= comissao_marketing

            if comissao_vendedor >= 1000:
                comissao_gerente = comissao_vendedor * 0.10
                comissao_vendedor -= comissao_gerente

            if cpf not in comissoes:
                comissoes[cpf] = {
                    'vendas_totais': 0,
                    'comissao_total': 0,
                    'comissao_marketing': 0,
                    'comissao_gerente': 0,
                }
            
            comissoes[cpf]['vendas_totais'] += valor_venda
            comissoes[cpf]['comissao_total'] += comissao_vendedor
            comissoes[cpf]['comissao_marketing'] += comissao_marketing
            comissoes[cpf]['comissao_gerente'] += comissao_gerente
        
        return comissoes
