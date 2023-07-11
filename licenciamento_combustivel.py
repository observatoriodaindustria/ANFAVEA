import pandas as pd
import datetime as dt
from valores_uteis import caminho_arquivo, nomes_planilhas, engine

nomes_colunas = ['nada', 'nada2', 'tipo_combustivel', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

# Data Frame utilizado como base
df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[3], names=nomes_colunas)

def criar_df_limpo_comb(ini_linha=0, tam_tabela=5, df=df_base, tipo_licenciamento=''):

    # Definfinindo a tabela
    df_limpo = df.drop(columns=nomes_colunas[:2]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_linha+1])
    df_limpo = df_limpo.drop(df_limpo.index[tam_tabela:])

    # Formatando a tabela
    df_unidirecional = df_limpo.melt(id_vars='tipo_combustivel', var_name='mes', value_name='quantidade')

    # Adicionando campos ao Data Frame
    df_unidirecional['ano'] = dt.datetime.now().year
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento
    df_unidirecional['dt_carga'] = dt.datetime.now()

    return df_unidirecional


def licenciamento_combustivel():
    # Licenciamento de Automoveis por quantidade:
    df_tot_auto_comerc_leve_comb = criar_df_limpo_comb(ini_linha=4, tipo_licenciamento='Total de automóveis e comerciais leves por combustível')
    df_tot_camin_onibus_comb = criar_df_limpo_comb(ini_linha=32, tam_tabela=3, tipo_licenciamento='Licenciamento total de caminhões e ônibus por combustível')
    df_resultado = pd.concat([df_tot_auto_comerc_leve_comb, df_tot_camin_onibus_comb]).reset_index(drop='True')
    df_resultado.to_sql('anfavea_lic_combus', if_exists='replace', index_label='id_combustiveis', schema='st', con=engine)