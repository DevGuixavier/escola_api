from config import db
from Alunos.alunos_model import Aluno  # Certifique-se de importar o modelo Aluno

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    professor = db.relationship('Professor', backref='turmas')

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo,
            'professor': self.professor.nome if self.professor else 'Professor não encontrado'
        }

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def adicionar_turma(turma_data):
    if 'descricao' not in turma_data or 'professor_id' not in turma_data:
        raise ValueError('Campos obrigatórios: descricao, professor_id')
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data.get('ativo', True)
    )
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    if 'descricao' in novos_dados:
        turma.descricao = novos_dados['descricao']
    if 'professor_id' in novos_dados:
        turma.professor_id = novos_dados['professor_id']
    if 'ativo' in novos_dados:
        turma.ativo = novos_dados['ativo']
    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    # Atualize ou remova os alunos associados à turma antes de excluir
    alunos = Aluno.query.filter_by(turma_id=turma.id).all()
    for aluno in alunos:
        db.session.delete(aluno)
    db.session.delete(turma)
    db.session.commit()
