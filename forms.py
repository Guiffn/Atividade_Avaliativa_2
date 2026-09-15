from flask_wtf import FlaskForm # Importa a classe base para criar formulários integrados ao Flask e protegidos contra CSRF.
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField # Importa os tipos de campos usados nos formulários.
from wtforms.validators import DataRequired, Email, EqualTo, Length # Importa regras que verificam se os dados preenchidos são válidos.

class RegisterForm(FlaskForm): # Define o formulário usado para cadastrar novos usuários.
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)]) # Campo de texto obrigatório com tamanho entre 2 e 20 caracteres.
    email = StringField('Email', validators=[DataRequired(), Email()]) # Campo obrigatório que precisa conter um email válido.
    senha = PasswordField('Senha', validators=[DataRequired()]) # Campo obrigatório para digitar a senha sem exibi-la na tela.
    confirm_senha = PasswordField('Confirme Senha', validators=[DataRequired(), EqualTo('senha')]) # Confirma a senha e verifica se ela é igual ao campo senha.
    submit = SubmitField('Sign Up') # Cria o botão usado para enviar o formulário.

class LoginForm(FlaskForm): # Define o formulário usado para autenticar um usuário existente.
    email = StringField('Email', validators=[DataRequired(), Email()]) # Recebe o email do usuário e verifica se ele é válido.
    senha = PasswordField('Senha', validators=[DataRequired()]) # Recebe a senha e exige que o campo seja preenchido.
    submit = SubmitField('Login') # Cria o botão de envio do formulário de login.

class TarefaForm(FlaskForm): # Define o formulário usado para criar e editar tarefas.
    titulo = StringField('Título', validators=[DataRequired(), Length(1, 140)]) # Campo obrigatório para o título, limitado a 140 caracteres.
    descricao = TextAreaField('Descrição') # Campo de texto maior para escrever a descrição da tarefa.
    status = SelectField('Status', choices=[('pendente', 'Pendente'), ('em andamento', 'Em Andamento'), ('concluída', 'Concluída')]) # Lista de status: o primeiro valor é salvo e o segundo é exibido.
    atribuido = SelectField('Atribuído a', coerce=int, choices=[]) # Lista de usuários; transforma o valor escolhido em inteiro e recebe opções no app.py.
    submit = SubmitField('Salvar') # Cria o botão para salvar a tarefa.