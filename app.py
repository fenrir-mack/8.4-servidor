import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from use_cases.livro_usecase import LivroUseCase
from infrastructure.txt_repository import TxtLivroRepository

app = Flask(__name__)
CORS(app)

db_path = os.path.join(os.path.dirname(__file__), 'infrastructure', 'banco.txt')
repository = TxtLivroRepository(filepath=db_path)
livro_usecase = LivroUseCase(repository)

@app.route("/livros", methods=["GET"])
def obter_livros():
    livros = livro_usecase.obter_todos_livros()
    return jsonify([livro.to_dict() for livro in livros]), 200

@app.route("/livros/filtrar", methods=["GET"])
def filtrar_livros():
    tipo = request.args.get("tipo")
    valor = request.args.get("valor")
    
    if tipo and valor:
        livros = livro_usecase.filtrar_livros(tipo, valor)
        return jsonify([livro.to_dict() for livro in livros]), 200
    return jsonify({"erro": "Parâmetros 'tipo' e 'valor' são obrigatórios"}), 400

@app.route("/livros", methods=["POST"])
def adicionar_livro():
    dados = request.json
    titulo = dados.get("titulo")
    autor = dados.get("autor")
    categoria = dados.get("categoria")
    editora = dados.get("editora")
    
    sucesso, msg = livro_usecase.adicionar_livro(titulo, autor, editora, categoria)
    if sucesso:
        return jsonify({"mensagem": msg}), 201
    else:
        return jsonify({"erro": msg}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
