# Desafio Técnico AAWZ - Backend

## Descrição
Este projeto foi desenvolvido para o desafio técnico da AAWZ, com o objetivo de criar um sistema de gerenciamento de vendedores e cálculos de comissões.

## Tecnologias Utilizadas
- Python
- Flask
- SQLAlchemy
- Pandas
- SQLite

## Instruções de Execução

### Configuração do Ambiente
1. Clone o repositório:
    ```sh
    git clone https://github.com/mateusfln/Desafio-tecnico-AAWZ-Backend
    ```
    e entre na pasta do projeto
    ```sh
    cd Desafio-tecnico-AAWZ-Backend
    ```

3. Instale as dependências:
    ```sh
    pip install pandas
    ```
    ```sh
    pip install flask
    ```
    ```sh
    pip install sqlalchemy
    ```

### Executando a Aplicação
1. Inicie o servidor Flask:
    ```sh
    python run.py
    ```

2. Acesse a API através de `http://localhost:5000`.

### Endpoints Disponíveis
- `GET /vendedores` - Retorna todos os vendedores registrados.
- `POST /vendedor` - Cria um novo vendedor.
- `GET /vendedor/<id>` - Retorna um vendedor pelo ID.
- `PUT /vendedor/<id>` - Atualiza um vendedor pelo ID.
- `DELETE /vendedor/<id>` - Deleta um vendedor pelo ID.
- `POST /importar-vendedores` - Importa vendedores de uma planilha.
- `POST /calcular-comissoes` - Calcula comissões de uma planilha de vendas.

### Testes
1. Para rodar os testes:
    ```sh
    pytest
    ```
    ou

   ```sh
    python -m pytest
    ```
