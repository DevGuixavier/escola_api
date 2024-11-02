from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from Turma.turma_model import Turma
from config import db

alunos_blueprint = Blueprint('alunos', __name__)

# ROTA PARA A PÁGINA INICIAL
@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    return render_template('index.html')

# ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos.html", alunos=alunos)

# ROTA PARA UM ALUNO ESPECÍFICO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# ROTA PARA ACESSAR O FORMULÁRIO DE CRIAÇÃO DE UM NOVO ALUNO
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('criar_Alunos.html')

# ROTA QUE CRIA UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        nome = request.form['nome']
        idade = int(request.form['idade'])
        turma_id = int(request.form['turma_id'])
        data_nascimento = request.form['data_nascimento']
        nota_primeiro_semestre = request.form.get('nota_primeiro_semestre', type=float)
        nota_segundo_semestre = request.form.get('nota_segundo_semestre', type=float)

        # Verificar se a turma existe
        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({'message': 'Turma não encontrada'}), 400
        
        # Verificar se as notas estão dentro do intervalo correto
        if nota_primeiro_semestre is not None and (nota_primeiro_semestre < 0 or nota_primeiro_semestre > 10):
            return jsonify({'message': 'Nota do primeiro semestre inválida. Deve estar entre 0 e 10.'}), 400
        if nota_segundo_semestre is not None and (nota_segundo_semestre < 0 or nota_segundo_semestre > 10):
            return jsonify({'message': 'Nota do segundo semestre inválida. Deve estar entre 0 e 10.'}), 400
        
        # Calcula a média se as notas foram fornecidas
        media_final = None
        if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
            media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
        
        # Cria o novo aluno
        novo_aluno = {
            'nome': nome,
            'idade': idade,
            'turma_id': turma_id,
            'data_nascimento': data_nascimento,
            'nota_primeiro_semestre': nota_primeiro_semestre,
            'nota_segundo_semestre': nota_segundo_semestre,
            'media_final': media_final
        }
        
        # Adiciona o aluno ao banco de dados
        adicionar_aluno(novo_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao processar a requisição', 'error': str(e)}), 500

# ROTA PARA ACESSAR O FORMULÁRIO DE EDIÇÃO DE UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# ROTA QUE EDITA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT', 'POST'])
def update_aluno(id_aluno):
    try:
        nome = request.form['nome']
        idade = int(request.form['idade'])
        turma_id = int(request.form['turma_id'])
        data_nascimento = request.form['data_nascimento']
        nota_primeiro_semestre = request.form.get('nota_primeiro_semestre', type=float)
        nota_segundo_semestre = request.form.get('nota_segundo_semestre', type=float)

        # Verificar se a turma existe
        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({'message': 'Turma não encontrada'}), 400

        # Verificar se as notas estão dentro do intervalo correto
        if nota_primeiro_semestre is not None and (nota_primeiro_semestre < 0 or nota_primeiro_semestre > 10):
            return jsonify({'message': 'Nota do primeiro semestre inválida. Deve estar entre 0 e 10.'}), 400
        if nota_segundo_semestre is not None and (nota_segundo_semestre < 0 or nota_segundo_semestre > 10):
            return jsonify({'message': 'Nota do segundo semestre inválida. Deve estar entre 0 e 10.'}), 400

        # Calcula a média se as notas foram fornecidas
        media_final = None
        if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
            media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
       
        # Cria o novo aluno
        novos_dados = {
            'nome': nome,
            'idade': idade,
            'turma_id': turma_id,
            'data_nascimento': data_nascimento,
            'nota_primeiro_semestre': nota_primeiro_semestre,
            'nota_segundo_semestre': nota_segundo_semestre,
            'media_final': media_final
        }
        
        # Atualiza o aluno no banco de dados
        atualizar_aluno(id_aluno, novos_dados)
        return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao processar a requisição', 'error': str(e)}), 500

# ROTA QUE DELETA UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['DELETE', 'POST'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao deletar aluno', 'error': str(e)}), 500

