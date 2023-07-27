import sqlalchemy as db
from urllib.parse import quote_plus
import datetime as dt

# Nomes das planilhas
nomes_planilhas = [
    'Índice',
    'I. Licenciamento',
    'II. Licenciamento Motorização',
    'III. Licenciamento Combustível',
    'IV. Licenciamento Empresa',
    'V. Exportação Volume',
    'VI. Produção',
    'VII. Outras informações'
]

# Parametros para a conexão
parametros = (
    # Driver que será utilizado na conexão
    'DRIVER={ODBC Driver 17 for SQL Server};'
    # IP ou nome do servidor\
    #'SERVER=192.168.23.194;'
    'SERVER=192.168.22.110;'
    # Porta
    'PORT=1433;'
    # Banco que será utilizado (Criar banco)
    'DATABASE=BD_OBSERVATORIO;'
    # Nome de usuário (Usuário default)
    'UID=USER_BD_OBSERVATORIO;'
    # Senha.
    'PWD=Observatorio@2022')


schema = 'st'
acao_insercao = 'append'
caminho_arquivo = 'arquivo/emplacamento.xlsx'
ano_atual = dt.datetime.now().year

# Criando conexão
url_db = quote_plus(parametros)
engine = db.create_engine(f'mssql+pyodbc:///?odbc_connect={url_db}')