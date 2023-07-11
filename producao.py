import pandas as pd
import datetime as dt
from valores_uteis import caminho_arquivo, nomes_planilhas, engine

nomes_colunas = ['nada', 'tipo_veiculo', 'veiculo_especifico', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[6], names=nomes_colunas)

def criar_df_limpo_produ(ini_linha, df=df_base, tipo_licenciamento='Produção de autoveículos'):
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_linha+1]).reset_index(drop=True)
    df_limpo.loc[1:4,'tipo_veiculo' ] = 'Veículos leves'
    df_limpo.loc[5:10,'tipo_veiculo' ] = 'Caminhões'
    df_limpo.loc[11:,'tipo_veiculo'] = 'Ônibus'
    
    # Resetando posições do dataframe  
    df_limpo.reset_index(drop=True)

    # Dropando outros valores
    df_limpo.drop(df_limpo.index[[0,1,2,5,11]], inplace=True)

    # Adicionando campos ao dataframe
    df_unidirecional = df_limpo.melt(['tipo_veiculo','veiculo_especifico'], var_name='mes', value_name='quantidade')
    df_unidirecional['tipo'] = tipo_licenciamento
    df_unidirecional['ano'] = dt.datetime.now().year
    df_unidirecional['dt_carga'] = dt.datetime.now()
    return df_unidirecional

def producao():
    df_export_vol = criar_df_limpo_produ(ini_linha=4)
    df_export_vol.to_sql('anfavea_producao', index_label='id_producao', schema='st', con=engine, if_exists='replace')
