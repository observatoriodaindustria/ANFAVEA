import pandas as pd
import datetime as dt
from valores_uteis import caminho_arquivo, nomes_planilhas, engine, schema, acao_insercao


nomes_colunas = ['nada', 'tipo_veiculo', 'veiculo_especifico', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']
df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[5], names=nomes_colunas)

def criar_df_limpo_exp(ini_linha, df=df_base,tipo_licenciamento='Exportações de autoveículos'):
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_linha+1]).reset_index(drop=True)
    df_limpo.loc[1:3,'tipo_veiculo' ] = 'Veículos leves'
    df_limpo.loc[4:9,'tipo_veiculo' ] = 'Caminhões'
    df_limpo.loc[10:12,'tipo_veiculo'] = 'Ônibus'
    df_limpo = df_limpo.drop(df_limpo.index[[0,1,4,10]]).reset_index(drop=True)

    # Adicionando campos ao dataframe
    df_unidirecional = df_limpo.melt(['tipo_veiculo','veiculo_especifico'], var_name='mes', value_name='quantidade')
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento
    df_unidirecional['ano'] = dt.datetime.now().year
    df_unidirecional['dt_carga'] = dt.datetime.now()
    return df_unidirecional

def export_volume():
    df_export_vol = criar_df_limpo_exp(ini_linha=4)
    df_export_vol.to_sql('anfavea_export_vol', index_label='id_export_vol', schema=schema, con=engine, if_exists=acao_insercao)