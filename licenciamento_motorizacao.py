import pandas as pd
import datetime as dt
from valores_uteis import engine, caminho_arquivo, nomes_planilhas, schema, acao_insercao


nomes_colunas = ['nada','tipo', 'unidades', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']
df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[2], names=nomes_colunas)

def licenciamento_motorizacao(ini_linha=5, tam_tabela=3, df=df_base, tipo_licenciamento='Licenciamento total de automóveis por motorização'):

    # Definfinindo a tabela
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1]).drop(columns=nomes_colunas[2])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_linha+1])
    df_limpo = df_limpo.drop(df_limpo.index[tam_tabela:])

    # Formatando a tabela
    df_unidirecional = df_limpo.melt(id_vars='tipo', var_name='mes', value_name='quantidade')
    df_unidirecional['dt_carga'] = dt.datetime.now()
    df_unidirecional['ano'] = dt.datetime.now().year
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento	
    df_unidirecional.to_sql('anfavea_lic_motorizacao', con=engine, schema=schema, if_exists=acao_insercao, index_label='id_motorizacao')

licenciamento_motorizacao()