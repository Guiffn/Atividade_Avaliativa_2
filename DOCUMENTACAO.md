# Trello Atividade

Documento de instalação, execução, uso e especificação da aplicação.

## 1. Visão geral

A aplicação é um gerenciador de tarefas desenvolvido com Flask. Ela permite:

- criar uma conta;
- entrar e sair do sistema;
- visualizar tarefas;
- filtrar tarefas por status;
- criar tarefas;
- editar tarefas;
- atribuir tarefas a usuários;
- excluir tarefas criadas pelo usuário atual.

## 2. Requisitos

- Python 3.11 ou superior;
- `pip`;
- PowerShell, Prompt de Comando ou terminal equivalente;
- navegador web.

O projeto foi validado com Python 3.14 e as dependências atuais do arquivo `requirements.txt`.

## 3. Estrutura do projeto

```text
Trello_atividade/
|-- app.py                  # Rotas e fluxo principal da aplicação
|-- config.py               # Configurações do Flask e do banco
|-- forms.py                # Formulários e validações
|-- models.py               # Modelos User e Tarefa
|-- requirements.txt        # Dependências Python
|-- app.db                  # Banco SQLite local, criado durante a execução
|-- Templates/              # Templates Jinja/HTML
|   |-- base.html
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- dashboard.html
|   |-- criar_tarefa.html
|   |-- editar_tarefa.html
|-- .venv/                  # Ambiente virtual local
```

## 4. Instalação

Abra o terminal na pasta do projeto:

```powershell
cd "C:\Users\5480\OneDrive\Desktop\FACULDADE\Python\Trello_atividade"
```

Crie o ambiente virtual, caso ele ainda não exista:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\activate
```

O terminal deverá mostrar algo semelhante a:

```text
(.venv) PS C:\...\Trello_atividade>
```

Instale as dependências usando o mesmo interpretador que executará o projeto:

```powershell
python -m pip install -r requirements.txt
```

O uso de `python -m pip` evita instalar os pacotes em outro Python por engano.

## 5. Verificação do interpretador

Confira qual Python está ativo:

```powershell
python -c "import sys; print(sys.executable)"
```

O caminho esperado termina com:

```text
Trello_atividade\.venv\Scripts\python.exe
```

Confira também se o Flask está instalado:

```powershell
python -c "import flask; print(flask.__version__)"
```

No VS Code, selecione `Ctrl+Shift+P` > `Python: Select Interpreter` e escolha:

```text
.venv\Scripts\python.exe
```

## 6. Configuração

As configurações estão em `config.py`.

### Chave secreta

A aplicação procura a variável de ambiente `SECRET_KEY`. Se ela não existir, usa o valor de desenvolvimento definido no código.

Para definir uma chave somente no terminal atual do PowerShell:

```powershell
$env:SECRET_KEY="coloque-uma-chave-grande-e-secreta"
```

Em produção, não publique a chave no repositório.

### Banco de dados

A aplicação procura a variável `DATABASE_URL`. Se ela não existir, usa um banco SQLite local:

```text
sqlite:///app.db
```

O arquivo `app.db` fica na pasta do projeto. Para outro banco, configure `DATABASE_URL` antes de iniciar a aplicação.

## 7. Execução

Com o ambiente virtual ativo, execute:

```powershell
python app.py
```

A aplicação será disponibilizada normalmente em:

```text
http://127.0.0.1:5000
```

Abra esse endereço no navegador. Para encerrar o servidor, pressione `Ctrl+C`.

Também é possível executar diretamente sem ativar o ambiente:

```powershell
.venv\Scripts\python.exe app.py
```

O modo `debug=True` está configurado para desenvolvimento. Não use esse modo em produção.

## 8. Fluxo de utilização

### 8.1 Criar uma conta

1. Acesse `/register` ou clique em `Registrar`.
2. Informe nome, email, senha e confirmação da senha.
3. O nome deve ter entre 2 e 20 caracteres.
4. O email deve ser válido e ainda não cadastrado.
5. As duas senhas devem ser iguais.
6. Envie o formulário.

A senha é armazenada como hash usando Werkzeug; a senha original não é salva.

### 8.2 Entrar

1. Acesse `/login`.
2. Informe o email e a senha cadastrados.
3. Após a autenticação, o sistema redireciona para `/dashboard`.

### 8.3 Criar uma tarefa

1. No dashboard, clique em `Criar nova tarefa`.
2. Informe o título, obrigatório, com até 140 caracteres.
3. Opcionalmente, informe a descrição.
4. Escolha um status:
   - `Pendente`;
   - `Em Andamento`;
   - `Concluída`.
5. Opcionalmente, atribua a tarefa a um usuário.
6. Clique em `Salvar`.

O usuário autenticado é registrado automaticamente como criador da tarefa.

### 8.4 Visualizar e filtrar

O dashboard mostra as tarefas ordenadas da mais recente para a mais antiga.

Use o campo de status para filtrar:

```text
/dashboard?status=pendente
/dashboard?status=em%20andamento
/dashboard?status=conclu%C3%ADda
```

A opção escolhida permanece selecionada depois que a página recarrega.

### 8.5 Editar

Na lista do dashboard, clique em `Editar` na tarefa desejada. É possível alterar:

- título;
- descrição;
- status;
- usuário atribuído.

Depois, clique em `Salvar`.

### 8.6 Excluir

Na lista do dashboard, clique em `Excluir`. A operação usa `POST` e exige login.

Por segurança, somente o usuário que criou a tarefa pode excluí-la. Um usuário diferente recebe erro HTTP `403`.

### 8.7 Sair

Clique em `Logout`. A sessão será encerrada e o usuário voltará para a página inicial.

## 9. Rotas da aplicação

| Método | Rota | Acesso | Função |
|---|---|---|---|
| `GET` | `/` | Público | Página inicial ou redirecionamento para o dashboard |
| `GET`, `POST` | `/register` | Público | Exibe e processa cadastro |
| `GET`, `POST` | `/login` | Público | Exibe e processa login |
| `GET` | `/logout` | Autenticado | Encerra a sessão |
| `GET` | `/dashboard` | Autenticado | Lista e filtra tarefas |
| `GET`, `POST` | `/tarefa/nova` | Autenticado | Cria uma tarefa |
| `GET`, `POST` | `/tarefa/<id>/editar` | Autenticado | Edita uma tarefa |
| `POST` | `/tarefa/<id>/excluir` | Autenticado e criador | Exclui uma tarefa |

## 10. Modelo de dados

### Usuário (`User`)

- `id`: identificador primário;
- `nome`: obrigatório e único;
- `email`: obrigatório e único;
- `senha`: hash da senha;
- `tarefa_criada`: relação com tarefas criadas;
- `tarefa_atribuida`: relação com tarefas atribuídas.

### Tarefa (`Tarefa`)

- `id`: identificador primário;
- `titulo`: obrigatório;
- `descricao`: opcional;
- `status`: começa como `pendente`;
- `criado_em`: preenchido automaticamente;
- `criador_id`: usuário que criou a tarefa;
- `atribuido_id`: usuário responsável, quando definido.

## 11. Validação técnica

Para verificar a sintaxe dos arquivos Python:

```powershell
python -m py_compile app.py config.py forms.py models.py
```

Para verificar se a aplicação pode ser importada:

```powershell
python -c "import app; print('Aplicação OK')"
```

O fluxo principal validado inclui:

- abertura das páginas inicial, login e cadastro;
- cadastro de usuário;
- login;
- acesso ao dashboard;
- criação de tarefa;
- filtragem por status;
- edição de tarefa;
- exclusão de tarefa.

## 12. Solução de problemas

### `ModuleNotFoundError: No module named 'flask'`

O pacote não está instalado no Python usado pelo terminal. Ative o ambiente e execute:

```powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### `AttributeError: module 'pkgutil' has no attribute 'get_loader'`

Esse erro ocorre quando Flask antigo é usado com Python 3.14. Atualize as dependências e confirme o interpretador:

```powershell
python -m pip install --upgrade -r requirements.txt
python -c "import sys; print(sys.executable)"
```

### `TemplateNotFound`

Confira se o nome do arquivo HTML corresponde exatamente ao nome usado em `render_template()` e se o arquivo está dentro de `Templates/`.

### Acesso ao dashboard redireciona para login

A rota `/dashboard` possui `login_required`. Faça login antes de acessá-la.

### Formulário não envia

Confira se:

- todos os campos obrigatórios foram preenchidos;
- o email é válido;
- a confirmação da senha é igual à senha;
- o formulário contém `{{ form.hidden_tag() }}`;
- o ambiente correto está ativo.

## 13. Observações para produção

Antes de publicar a aplicação:

- use uma `SECRET_KEY` forte configurada por variável de ambiente;
- não use `debug=True`;
- não publique `app.db` se ele contiver dados reais;
- use migrações para alterações no banco;
- utilize um servidor WSGI apropriado;
- revise permissões de edição e exclusão;
- aumente o tamanho da coluna de hash de senha para `String(255)` antes de criar uma nova base de produção.
