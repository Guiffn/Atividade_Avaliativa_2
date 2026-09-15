from flask import abort #Import serve para retornar um erro 403 caso o usuário tente excluir uma tarefa que não é dele, ou seja uma acesso proibido.
from flask import Flask, render_template, redirect, url_for, flash, request #Flask o que cria a aplicação | Render_template para renderizar os templates HTML | Redirect para redirecionar o usuário para outra rota | url_for para gerar URLs para as rotas | flash para exibir mensagens temporárias | request para acessar dados da requisição
from config import Config # Importa a classe da configuração do aplicativo. Contem chave secreta e configuração do banco de dados.
from models import Tarefa, db, User # Importe User: modelo da tabela de usúario, Tarefa: modelo da tabela de tarefas, db: objeto do banco de dados.
from forms import RegisterForm, LoginForm, TarefaForm #Importa formulários criados com o flask WTF para registro, login e criação/edição de tarefas.
from flask_migrate import Migrate # Importe Migrate: para gerenciar migrações do banco de dados, permitindo criar e atualizar tabelas conforme os modelos definidos.
from flask_login import LoginManager, login_user, logout_user, login_required, current_user #Importa recursos para autenticaçãpo

app = Flask(__name__)
app.config.from_object(Config)  #Cria o objeto principal da aplicação flask, __name__  informa ao flask onde o arquivo atual esta localizado. Config carrega as configurações da aplicação, como a chave secreta e a URI do banco de dados.

db.init_app(app) 
migrate = Migrate(app, db) #Conecta o banco de dados com a aplicação Flask e permite gerenciar migrações do banco de dados.

login_manager = LoginManager(app)
login_manager.login_view = 'login' # Cria o objeto de gerenciamento de login, que lida com a autenticação do usuário. Define a rota de login padrão para redirecionar usuários não autenticados.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # Busca no banco o usuário pelo ID salvo na sessão de login.

@app.route('/') # Rota inicial da aplicação. Conecta a URL com a função 
def index(): # Executa http://127.0.0.1:5000/ 
    if current_user.is_authenticated:         # Verifica se o usuário está autenticado. Se estiver, redireciona para o dashboard.
        return redirect(url_for('dashboard'))
    return render_template('index.html') # Se não estiver autenticado, renderiza a página inicial (index.html) com opções de login e registro.

@app.route('/register', methods=['GET', 'POST']) # Rota de cadastro de usuário. Aceita métodos GET e POST. GET somente exibe o formulário de registro, enquanto POST processa os dados enviados pelo formulário.
def register():
    form = RegisterForm() #Cria formulario de cadastro de usuário. O formulário é definido na classe RegisterForm, que contém campos para nome, email, senha e confirmação de senha.
    if form.validate_on_submit():  # Verifica se o formulário foi enviado e se os dados são válidos. Se sim, prossegue com o registro do usuário.
        if User.query.filter_by(email=form.email.data).first(): # Verifica se já existe um usuário com o mesmo email no banco de dados. Se existir, exibe uma mensagem de erro e redireciona de volta para a página de registro.
            flash('Usuario já existe!')
            return redirect(url_for('register'))
        user = User(nome=form.nome.data, email=form.email.data)
        user.set_senha(form.senha.data) # PEga a senha do usuário, gera um hash seguro e armazena no banco de dados. Isso garante que a senha não seja armazenada em texto simples, aumentando a segurança.
        db.session.add(user)   # Adiciona o novo usuário à sessão do banco de dados, preparando-o para ser salvo.
        db.session.commit() # Salva as alterações no banco de dados, efetivamente criando o novo usuário.
        flash('Conta criada com sucesso! Faça login.')
        return redirect(url_for('login')) #Redireciona o usuário para a página de login após o registro bem-sucedido.
    return render_template('register.html', form=form) # Renderiza o template de registro (register.html) e passa o formulário para que ele seja exibido na página. Se houver erros de validação, eles serão mostrados ao usuário.

@app.route('/login', methods=['GET', 'POST']) # Rota de login de usuário. Aceita métodos GET e POST. GET exibe o formulário de login, enquanto POST processa os dados enviados pelo formulário.
def login():
    form = LoginForm() # Cria o formulário usado para receber email e senha.
    if form.validate_on_submit(): # Verifica se o formulário foi enviado e se os dados são válidos.
        user = User.query.filter_by(email=form.email.data).first() # Procura no banco um usuário com o email informado.
        if user is None or not user.check_senha(form.senha.data): # Verifica se o usuário existe e se a senha está correta.
            flash('Login inválido. Verifique seu email e senha.') # Exibe uma mensagem quando os dados de login estão incorretos.
            return redirect(url_for('login')) # Retorna o usuário para a página de login.
        login_user(user) # Cria a sessão de login para o usuário autenticado.
        return redirect(url_for('dashboard')) # Após o login, encaminha o usuário para o dashboard.
    return render_template('login.html', form=form) # Exibe o formulário de login, inclusive quando existem erros de validação.

@app.route('/logout') # Rota responsável por encerrar a sessão do usuário.
@login_required # Exige que o usuário esteja logado para acessar esta rota.
def logout():
    logout_user() # Remove o usuário atual da sessão de login.
    return redirect(url_for('index')) # Redireciona o usuário para a página inicial.

@app.route('/dashboard') # Rota que exibe o painel principal do sistema.
@login_required # Impede que usuários não autenticados acessem o dashboard.
def dashboard():
    todas_tarefas = Tarefa.query.order_by(Tarefa.criado_em.desc()).all() # Busca todas as tarefas, começando pelas mais recentes.
    minha_tarefa = Tarefa.query.filter( # Busca as tarefas criadas ou atribuídas ao usuário atualmente logado.
        (Tarefa.criador_id == current_user.id) |
        (Tarefa.atribuido_id == current_user.id)
    ).all() # Executa a consulta e transforma o resultado em uma lista.
    status_filter = request.args.get('status') # Lê da URL o status escolhido no filtro.
    if status_filter: # Verifica se o usuário selecionou algum status.
        todas_tarefas = [t for t in todas_tarefas if t.status == status_filter] # Mantém somente as tarefas com o status escolhido.
    return render_template('dashboard.html', todas_tarefas=todas_tarefas, minha_tarefa=minha_tarefa) # Envia as tarefas para o template do dashboard.

@app.route('/tarefa/nova', methods=['GET', 'POST']) # Rota usada para abrir e enviar o formulário de nova tarefa.
@login_required # Somente usuários autenticados podem criar tarefas.
def criar_tarefa():
    form = TarefaForm() # Cria o formulário de tarefas.
    user = User.query.all() # Busca todos os usuários para montar a lista de atribuição.
    form.atribuido.choices = [(0, '--Nenhum--')] + [(u.id, u.nome) for u in user] # Define as opções do campo de usuário atribuído.
    if form.validate_on_submit(): # Verifica se o formulário foi enviado e passou nas validações.
        atribuido_id = form.atribuido.data or None # Obtém o ID do usuário escolhido ou define None se estiver vazio.
        if atribuido_id == 0: # Verifica se a opção escolhida foi '--Nenhum--'.
            atribuido_id = None # Salva None no banco quando nenhuma pessoa foi escolhida.
        tarefa = Tarefa(titulo=form.titulo.data, descricao=form.descricao.data, # Cria uma nova tarefa com o título e a descrição informados.
                        status= form.status.data, criador_id= current_user.id, 
                        atribuido_id= atribuido_id) # Define o status, o criador e o usuário atribuído.
        db.session.add(tarefa) # Adiciona a nova tarefa à sessão do banco.
        db.session.commit() # Confirma e salva a tarefa no banco de dados.
        flash('Tarefa criada com sucesso!', 'success') # Exibe uma mensagem de sucesso para o usuário.
        return redirect(url_for('dashboard')) # Volta para o dashboard depois de criar a tarefa.
    return render_template('criar_tarefa.html', form=form) # Exibe o formulário quando ele ainda não foi enviado ou possui erros.

@app.route('/tarefa/<int:tarefa_id>/editar', methods=['GET', 'POST']) # Rota para abrir e enviar a edição de uma tarefa específica.
@login_required # Somente usuários autenticados podem editar tarefas.
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id) # Busca a tarefa pelo ID ou retorna erro 404 se ela não existir.
    form = TarefaForm(obj=tarefa) # Preenche o formulário com os dados atuais da tarefa.
    users = User.query.all() # Busca todos os usuários para preencher a lista de atribuição.
    form.atribuido.choices = [(0, '--Nenhum--')] + [(u.id, u.nome) for u in users] # Define as opções do campo de usuário atribuído.
    form.atribuido.data = tarefa.atribuido_id or 0 # Seleciona no formulário o usuário já atribuído à tarefa.
    if form.validate_on_submit(): # Verifica se o formulário de edição foi enviado e é válido.
        tarefa.titulo = form.titulo.data # Atualiza o título da tarefa.
        tarefa.descricao = form.descricao.data # Atualiza a descrição da tarefa.
        tarefa.status = form.status.data # Atualiza o status da tarefa.
        tarefa.atribuido_id = form.atribuido.data if form.atribuido.data != 0 else None # Atualiza o usuário atribuído ou remove a atribuição.
        db.session.commit() # Salva as alterações no banco de dados.
        flash('Tarefa atualizada com sucesso!', 'success') # Exibe uma mensagem confirmando a atualização.
        return redirect(url_for('dashboard')) # Volta para o dashboard depois de editar a tarefa.
    return render_template('editar_tarefa.html', form=form, tarefa=tarefa) # Exibe o formulário preenchido para edição.

@app.route('/tarefa/<int:tarefa_id>/excluir', methods=['POST']) # Rota responsável por excluir uma tarefa específica.
@login_required # Somente usuários autenticados podem tentar excluir tarefas.
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id) # Busca a tarefa pelo ID ou retorna erro 404 se ela não existir.
    if tarefa.criador_id != current_user.id: # Verifica se o usuário logado é o criador da tarefa.
        abort(403) # Bloqueia a exclusão se a tarefa pertencer a outro usuário.
    db.session.delete(tarefa) 
    db.session.commit() 
    flash('Tarefa excluída com sucesso!', 'success') # Exibe uma mensagem confirmando a exclusão.
    return redirect(url_for('dashboard')) # Volta para o dashboard após excluir a tarefa.


if __name__ == '__main__': # Verifica se este arquivo está sendo executado diretamente.
    with app.app_context(): # Cria um contexto para permitir o acesso ao banco pela aplicação.
        db.create_all() # Cria as tabelas do banco que ainda não existem.
    app.run(debug=True) # Inicia o servidor Flask em modo de desenvolvimento.