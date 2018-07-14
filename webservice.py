from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources = {r"/*": {"origins": "*"}})

tarefas = [
    {'codigo': 1, 'descricao': "tarefa 1"},
    {'codigo': 2, 'descricao': "tarefa 2"},
    {'codigo': 3, 'descricao': "tarefa 3"}
]


def encontrar(codigo: int):
    for tarefa in tarefas:
        if int(tarefa['codigo']) == int(codigo):
            return tarefa


def remover(codigo: int):
    index = 0
    for tarefa in tarefas:
        if int(tarefa['codigo']) == int(codigo):
            tarefas.pop(index)
            return True
        index += 1
    return False


@app.route('/')
def listar():
    return jsonify(tarefas)


@app.route('/<codigo>', methods=['GET'])
def obter(codigo):
    tarefa = encontrar(codigo)

    try:
        tarefa
    except:
        return jsonify({'success': False, 'message': "Não encontrado"}), 400
    else:
        return jsonify(tarefa), 200


@app.route('/', methods=['POST'])
def inserir():
    descricao = request.json['descricao']
    codigo = int(tarefas[len(tarefas) - 1]['codigo']) + 1
    tarefa = {'codigo': codigo, 'descricao': descricao}
    tarefas.append(tarefa)

    return jsonify({'success': True}), 200;


@app.route('/<codigo>', methods=['PUT'])
def editar(codigo: int):
    descricao = request.json['descricao']
    tarefa = encontrar(codigo)

    try:
        tarefa['descricao'] = descricao
    except:
        return jsonify({'success': False, 'message': "Não encontrado"}), 400
    else:
        return jsonify({'success': True}), 200;


@app.route('/<codigo>', methods=['DELETE'])
def excluir(codigo: int):
    try:
        if remover(codigo) == False:
            raise Exception("Não encontrado")
    except:
        return jsonify({'success': False, 'message': "Não encontrado"})
    else:
        return jsonify({'success': True})


@app.route('/index')
def index():
    return "Hello world"


app.run(debug=True)