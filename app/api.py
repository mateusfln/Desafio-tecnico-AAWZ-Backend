from flask import Flask, request, jsonify
from .crud import GerenciadorVendedores
from .planilha_handler import PlanilhaHandler

app = Flask(__name__)
gerenciador = GerenciadorVendedores()

@app.route('/vendedores', methods=['GET'])
def get_vendedores():
    vendedores = gerenciador.get_vendedores()
    if vendedores:
        return jsonify([vendedor.to_dict() for vendedor in vendedores])
    else:
        return jsonify({"error": "Nao existem registros de vendedores ainda"}), 404

@app.route('/vendedor', methods=['POST'])
def create_vendedor():
    data = request.get_json()
    vendedor = gerenciador.create_vendedor(
        nome=data['nome'],
        cpf=data['cpf'],
        data_nascimento=data['data_nascimento'],
        email=data['email'],
        estado=data['estado']
    )
    return jsonify(vendedor.to_dict())

@app.route('/vendedor/<int:id>', methods=['GET'])
def get_vendedor(id):
    vendedor = gerenciador.get_vendedor(id)
    if vendedor:
        return jsonify(vendedor.to_dict())
    else:
        return jsonify({"error": "Vendedor não encontrado"}), 404

@app.route('/vendedor/<int:id>', methods=['PUT'])
def update_vendedor(id):
    data = request.get_json()
    vendedor = gerenciador.update_vendedor(
        vendedor_id=id,
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento'),
        email=data.get('email'),
        estado=data.get('estado')
    )
    return jsonify(vendedor.to_dict())

@app.route('/vendedor/<int:id>', methods=['DELETE'])
def delete_vendedor(id):
    vendedor = gerenciador.delete_vendedor(id)
    if vendedor:
        return jsonify({"message": "Vendedor deletado com sucesso"})
    else:
        return jsonify({"error": "Vendedor não encontrado"}), 404

@app.route('/importar-vendedores', methods=['POST'])
def importar_vendedores():
    data = request.get_json()
    path = data.get('path')
    handler = PlanilhaHandler()
    handler.importar_vendedores(path)
    return jsonify({"message": "Vendedores importados com sucesso"})

@app.route('/calcular-comissoes', methods=['POST'])
def calcular_comissoes():
    data = request.get_json()
    path = data.get('path')
    handler = PlanilhaHandler()
    comissoes = handler.calcular_comissoes(path)
    return jsonify(comissoes)

if __name__ == '__main__':
    app.run(debug=True)
