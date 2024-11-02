from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .Professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor
from config import db

professores_blueprint = Blueprint('professores', __name__)

# ROTA PRINCIPAL
@professores_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Bem vindo à API de professores"

# ROTA PARA TODOS OS PROFESSORES
@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template("professores.html", professores=professores)

# ROTA PARA UM PROFESSOR ESPECÍFICO
@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# ROTA PARA ACESSAR O FORMULÁRIO DE CRIAÇÃO DE UM NOVO PROFESSOR
@professores_blueprint.route('/professores/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('criar_Professores.html')

# ROTA QUE CRIA UM NOVO PROFESSOR
@professores_blueprint.route('/professores', methods=['POST'])
def create_professor():
    try:
        nome = request.form['nome']
        idade = int(request.form['idade'])
        materia = request.form['materia']
        observacoes = request.form.get('observacoes', '')

        novo_professor = {
            'nome': nome,
            'idade': idade,
            'materia': materia,
            'observacoes': observacoes
        }

        adicionar_professor(novo_professor)
        return redirect(url_for('professores.get_professores'))
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao processar a requisição', 'error': str(e)}), 500

# ROTA PARA ACESSAR O FORMULÁRIO DE EDIÇÃO DE UM PROFESSOR
@professores_blueprint.route('/professores/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# ROTA QUE EDITA UM PROFESSOR
@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT', 'POST'])
def update_professor(id_professor):
    try:
        nome = request.form['nome']
        idade = int(request.form['idade'])
        materia = request.form['materia']
        observacoes = request.form.get('observacoes', '')

        novos_dados = {
            'nome': nome,
            'idade': idade,
            'materia': materia,
            'observacoes': observacoes
        }

        atualizar_professor(id_professor, novos_dados)
        return redirect(url_for('professores.get_professor', id_professor=id_professor))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao processar a requisição', 'error': str(e)}), 500


# ROTA QUE DELETA UM PROFESSOR
@professores_blueprint.route('/professores/delete/<int:id_professor>', methods=['DELETE', 'POST'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return redirect(url_for('professores.get_professores'))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao deletar professor', 'error': str(e)}), 500
