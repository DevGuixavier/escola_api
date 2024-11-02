import os
from config import app, db
from Alunos.alunos_routes import alunos_blueprint
from Professor.professor_routes import professores_blueprint
from Turma.turma_routes import turmas_blueprint


# Registrar os blueprints
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)

# Criar todas as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Executar a aplicação
if __name__ == '__main__':
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get('PORT', 8000), debug=app.config.get('DEBUG', True))