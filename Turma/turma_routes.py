from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .turma_model import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turmas_blueprint = Blueprint('turmas', __name__)

# Listar turmas em JSON
@turmas_blueprint.route('/api/turmas', methods=['GET'])
def get_turmas_json():
    return jsonify(listar_turmas())

# Listar turmas em HTML
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas_html():
    turmas = listar_turmas()
    return render_template("turmas.html", turmas=turmas)

# Detalhes de uma turma em JSON
@turmas_blueprint.route('/api/turmas/<int:id_turma>', methods=['GET'])
def get_turma_json(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

# Detalhes de uma turma em HTML
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma_html(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template("turma_id.html", turma=turma)
    except TurmaNaoEncontrada:
        return render_template("turma_id.html", error="Turma não encontrada"), 404

# Página para adicionar nova turma
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template("criar_Turmas.html")

# Criação de turma em HTML
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma_html():
    try:
        descricao = request.form['descricao']
        professor_id = int(request.form['professor_id'])
        ativo = request.form['ativo'].lower() == 'true'

        nova_turma = {
            'descricao': descricao,
            'professor_id': professor_id,
            'ativo': ativo
        }

        adicionar_turma(nova_turma)
        return redirect(url_for('turmas.get_turmas_html'))
    except ValueError as e:
        return render_template("criar_Turmas.html", error=str(e))

# Criação de turma em JSON
@turmas_blueprint.route('/api/turmas', methods=['POST'])
def create_turma_json():
    data = request.json
    if 'descricao' not in data or 'professor_id' not in data:
        return jsonify({'message': 'Campos obrigatórios: descricao, professor_id'}), 400
    try:
        adicionar_turma(data)
        return jsonify(data), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# Rota para deletar uma turma
@turmas_blueprint.route('/turmas/<int:id_turma>/deletar', methods=['POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas_html'))
    except TurmaNaoEncontrada:
        return render_template("turmas.html", error="Turma não encontrada"), 404

# Página para editar uma turma
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template("turma_update.html", turma=turma)
    except TurmaNaoEncontrada:
        return render_template("turmas.html", error="Turma não encontrada"), 404

# Atualizar turma em HTML
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['POST'])
def update_turma_html(id_turma):
    try:
        descricao = request.form['descricao']
        professor_id = int(request.form['professor_id'])
        ativo = request.form['ativo'].lower() == 'true'

        turma_atualizada = {
            'descricao': descricao,
            'professor_id': professor_id,
            'ativo': ativo
        }

        atualizar_turma(id_turma, turma_atualizada)
        return redirect(url_for('turmas.get_turma_html', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return render_template("turma_update.html", error="Turma não encontrada", turma_id=id_turma), 404
    except ValueError as e:
        return render_template("turma_update.html", error=str(e), turma_id=id_turma)

# Atualizar turma em JSON
@turmas_blueprint.route('/api/turmas/<int:id_turma>', methods=['PUT'])
def update_turma_json(id_turma):
    data = request.json
    if 'descricao' not in data or 'professor_id' not in data:
        return jsonify({'message': 'Campos obrigatórios: descricao, professor_id'}), 400
    try:
        atualizar_turma(id_turma, data)
        return jsonify(data), 200
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
