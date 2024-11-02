from config import db
from datetime import datetime

# Modelo de dados para a tabela aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=True)
    nota_segundo_semestre = db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)  # Adicionando data_nascimento como uma coluna
    turma = db.relationship('Turma', backref='alunos')
    
    # Método para retornar um dicionário com os dados do aluno
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),  # Garantindo o formato correto
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final
        }

# Exceção para quando o aluno não é encontrado
class AlunoNaoEncontrado(Exception):
    pass

# Validações manuais
def validar_aluno(aluno_data):
    if not aluno_data.get('nome'):
        raise ValueError("O nome é obrigatório.")
    if not isinstance(aluno_data.get('idade'), int) or aluno_data['idade'] <= 0:
        raise ValueError("A idade deve ser um número inteiro positivo.")
    if not aluno_data.get('turma_id'):
        raise ValueError("O ID da turma é obrigatório.")
    if aluno_data.get('nota_primeiro_semestre') is not None:
        if aluno_data['nota_primeiro_semestre'] < 0 or aluno_data['nota_primeiro_semestre'] > 10:  # Correção aqui
            raise ValueError("A nota do primeiro semestre deve estar entre 0 e 10.")
    if aluno_data.get('nota_segundo_semestre') is not None:
        if aluno_data['nota_segundo_semestre'] < 0 or aluno_data['nota_segundo_semestre'] > 10:  # Correção aqui
            raise ValueError("A nota do segundo semestre deve estar entre 0 e 10.")
    if not aluno_data.get('data_nascimento'):
        raise ValueError("A data de nascimento é obrigatória.")
    
    # Converter data_nascimento para o tipo date
    aluno_data['data_nascimento'] = datetime.strptime(aluno_data['data_nascimento'], '%Y-%m-%d').date()

# Funções para manipular os dados da tabela aluno
def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

# Função para listar todos os alunos
def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

# Função para adicionar um novo aluno
def adicionar_aluno(aluno_data):

    # Validação manual dos dados
    validar_aluno(aluno_data)

    # Criação do aluno se os dados forem válidos
    novo_aluno = Aluno(
        nome=aluno_data['nome'],
        idade=aluno_data['idade'],
        turma_id=aluno_data['turma_id'],
        data_nascimento=aluno_data['data_nascimento'],
        nota_primeiro_semestre=aluno_data.get('nota_primeiro_semestre'),
        nota_segundo_semestre=aluno_data.get('nota_segundo_semestre'),
        media_final=aluno_data.get('media_final')
    )
    
    # Se as notas foram fornecidas, calcula a média final
    if novo_aluno.nota_primeiro_semestre is not None and novo_aluno.nota_segundo_semestre is not None:
        novo_aluno.media_final = (novo_aluno.nota_primeiro_semestre + novo_aluno.nota_segundo_semestre) / 2
    
    db.session.add(novo_aluno)
    db.session.commit()

# Função para atualizar os dados de um aluno
def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    
    # Validação manual dos novos dados
    validar_aluno(novos_dados)

    # Atualização dos dados do aluno
    aluno.nome = novos_dados['nome']
    aluno.idade = novos_dados.get('idade', aluno.idade)
    aluno.turma_id = novos_dados.get('turma_id', aluno.turma_id)
    aluno.data_nascimento = novos_dados.get('data_nascimento', aluno.data_nascimento)
    aluno.nota_primeiro_semestre = novos_dados.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = novos_dados.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    
    # Atualizar a média final se as notas estiverem presentes
    if aluno.nota_primeiro_semestre is not None and aluno.nota_segundo_semestre is not None:
        aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
    else:
        aluno.media_final = None  # Define como None se as notas não estiverem completas
    
    # Salva as alterações no banco de dados
    db.session.commit()

# Função para excluir um aluno
def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()
