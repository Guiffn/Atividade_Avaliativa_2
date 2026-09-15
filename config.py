import os  #Importa módulo que permite interagir com o sistema operacional, como acessar variáveis de ambiente e manipular caminhos de arquivos.
basedir = os.path.abspath(os.path.dirname(__file__)) # Essa linha calcula o caminho absoluto do diretório onde o arquivo de configuração está localizado, armazenando-o na variável basedir. Isso é útil para construir caminhos de arquivos relativos ao diretório do projeto.

class Config: # Define a classe Config que contém as configurações da aplicação Flask.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'troque_essa_chave' # Define a chave secreta usada pelo Flask para proteger sessões e formulários contra ataques CSRF. Ela é obtida de uma variável de ambiente, e se não estiver definida, um valor padrão é usado (o que não é seguro para produção).
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # Define a URI de conexão com o banco de dados. Primeiro, tenta obter a URL do banco de dados de uma variável de ambiente (útil para produção). Se não estiver definida, usa um banco de dados SQLite local chamado 'app.db' no diretório do projeto.
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desativa o recurso de rastreamento de modificações do SQLAlchemy, que consome recursos adicionais e não é necessário na maioria dos casos. Isso ajuda a melhorar o desempenho da aplicação.
