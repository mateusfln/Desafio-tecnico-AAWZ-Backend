import pandas as pd
from .crud import GerenciadorVendedores

class PlanilhaHandler:
    def __init__(self):
        self.gerenciador = GerenciadorVendedores()

    def importar_vendedores(self, path):
        df = pd.read_excel(path)

        for _, row in df.iterrows():
            try:
                if row['cpf'] != None:
                    vendedor = self.gerenciador.get_vendedor_by_cpf(row['cpf'])
                    self.gerenciador.update_vendedor(
                        vendedor_id=vendedor.id,
                        nome=row['nome'],
                        cpf=row['cpf'],
                        data_nascimento=row['data_nascimento'],
                        email=row['email'],
                        estado=row['estado']
                )
                else: 
                    self.gerenciador.create_vendedor(
                        nome=row['nome'],
                        cpf=row['cpf'],
                        data_nascimento=row['data_nascimento'],
                        email=row['email'],
                        estado=row['estado']
                    )
            except ValueError:
                return ValueError

    def converter_valor(self, valor):
            if isinstance(valor, str):
                valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
                return float(valor) if valor else 0.0
            return float(valor)
               
    def calcular_volume_e_media_vendas(self, path):
        df_vendas = pd.read_excel(path)

        df_vendas['Valor da Venda'] = df_vendas['Valor da Venda'].apply(self.converter_valor)
        result = df_vendas.groupby(['Nome do Vendedor', 'Canal de Venda']).agg(
            volume_vendas=('Valor da Venda', 'sum'),
            numero_vendas=('Valor da Venda', 'count'),
            media_vendas=('Valor da Venda', 'mean')
        ).reset_index()
        return result.to_dict(orient='records')
    
    def calcular_comissoes(self, path):
        df = pd.read_excel(path)
        comissoes = {}
        for _, row in df.iterrows():
            nome_vendedor = row['Nome do Vendedor']
            valor_venda = self.converter_valor(row['Valor da Venda'])
            canal = row['Canal de Venda']

            comissao_vendedor = valor_venda * 0.10
            comissao_marketing = 0
            comissao_gerente = 0

            if canal == 'Online':
                comissao_marketing = comissao_vendedor * 0.20
                comissao_vendedor -= comissao_marketing

            if comissao_vendedor >= 1000:
                comissao_gerente = comissao_vendedor * 0.10
                comissao_vendedor -= comissao_gerente

            if nome_vendedor not in comissoes:
                comissoes[nome_vendedor] = {
                    'vendas_totais': 0,
                    'comissao_total': 0,
                    'comissao_marketing': 0,
                    'comissao_gerente': 0,
                }
            comissoes[nome_vendedor]['vendas_totais'] += valor_venda
            comissoes[nome_vendedor]['comissao_total'] += comissao_vendedor
            comissoes[nome_vendedor]['comissao_marketing'] += comissao_marketing
            comissoes[nome_vendedor]['comissao_gerente'] += comissao_gerente
        
        return comissoes
