from flask_sqlalchemy import SQLAlchemy # Importa a extensão que conecta os modelos Python ao banco de dados.
from flask_login import UserMixin # Fornece métodos necessários para um objeto User funcionar com o Flask-Login.
from datetime import datetime # Permite registrar a data e a hora de criação das tarefas.
from werkzeug.security import generate_password_hash, check_password_hash # Importa funções para proteger e verificar senhas.



db = SQLAlchemy() # Cria o objeto do banco, que será conectado à aplicação no app.py.

class User(UserMixin, db.Model): # Define o modelo que representa a tabela de usuários no banco.
    id = db.Column(db.Integer, primary_key=True) # Identificador único de cada usuário.
    nome = db.Column(db.String(64), unique=True, nullable=False) # Nome obrigatório e que não pode se repetir.
    email = db.Column(db.String(120), unique=True, nullable=False) # Email obrigatório e único para cada usuário.
    senha = db.Column(db.String(60), nullable=False) # Armazena o hash da senha, não a senha original.
    tarefa_criada = db.relationship('Tarefa', backref='criador', lazy='dynamic', foreign_keys='Tarefa.criador_id') # Relaciona o usuário às tarefas que ele criou.
    tarefa_atribuida = db.relationship('Tarefa', backref='atribuido', lazy='dynamic', foreign_keys='Tarefa.atribuido_id') # Relaciona o usuário às tarefas atribuídas a ele.

    def set_senha(self, senha): # Recebe a senha original e prepara seu armazenamento seguro.
        self.senha = generate_password_hash(senha) # Gera um hash da senha antes de salvar no banco.

    def check_senha(self, senha): # Compara uma senha informada com o hash salvo no banco.
        return check_password_hash(self.senha, senha) # Retorna True se a senha estiver correta e False caso contrário.

class Tarefa(db.Model): # Define o modelo que representa a tabela de tarefas no banco.
    id = db.Column(db.Integer, primary_key=True) # Identificador único da tarefa.
    titulo = db.Column(db.String(100), nullable=False) # Título obrigatório da tarefa, limitado a 100 caracteres.
    descricao = db.Column(db.Text) # Texto da descrição; pode ser maior e não é obrigatório.
    status = db.Column(db.String(20), default='pendente') # Status da tarefa, com 'pendente' como valor inicial.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow) # Data e hora preenchidas automaticamente na criação.
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id')) # ID do usuário que criou a tarefa.
    atribuido_id = db.Column(db.Integer, db.ForeignKey('user.id')) # ID do usuário responsável pela tarefa, se houver.