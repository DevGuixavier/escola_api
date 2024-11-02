import unittest
from flask_testing import TestCase
from config import app, db
from Turma.turma_routes import turmas_blueprint
from Professor.Professor_model import Professor

# Classe de teste para a rota de turmas
class TurmaTestCase(TestCase):
   
    # Configuração da aplicação para os testes
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.register_blueprint(turmas_blueprint)
        return app
    
    # Configuração do banco de dados para os testes
    def setUp(self):
        db.create_all()
    
        # Cria um professor para associar as turmas
        professor = Professor(nome="Professor Teste", idade=30, materia="Matemática")
        db.session.add(professor)
        db.session.commit()
        
        # Adiciona uma turma para testar
        turma = {
            'descricao': 'Turma Teste',
            'professor_id': professor.id,
            'ativo': True
        }
        # Insere a turma no banco de dados
        db.session.execute(
            'INSERT INTO turma (descricao, professor_id, ativo) VALUES (:descricao, :professor_id, :ativo)',
            turma
        )
        db.session.commit()

    # Limpa o banco de dados após os testes
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Testa a rota de listagem de turmas
    def test_get_turmas(self):
        response = self.client.get('/api/turmas')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Turma Teste', response.data)  # Verifica se a descrição da turma está na resposta

# Testa a rota de listagem de turmas
if __name__ == '__main__':
    unittest.main()
