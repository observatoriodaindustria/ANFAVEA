import pandas as pd
import datetime as dt
from valores_uteis import caminho_arquivo, nomes_planilhas, engine, schema, acao_insercao
from download_arquivo import ano_atual


nomes_colunas = ['nada', 'tipo_veiculo', 'veiculo_especifico', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

def criar_df_limpo(ini_linha, df, tam_tabela=10 ,tipo_licenciamento=''):
    
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_linha+1])
    df_limpo = df_limpo.drop(df_limpo.index[tam_tabela:])

    # Resentando os índices
    df_limpo = df_limpo.reset_index(drop=True)
    
    # Preenchendo campos do Tipo do veículo
    df_limpo.loc[:2 ,'tipo_veiculo'] = 'Veículos leves' 
    df_limpo.loc[4:8 ,'tipo_veiculo'] = 'Caminhões' 
    df_limpo.loc[9 ,'veiculo_especifico'] = 'Ônibus' 

    # Removendo outros valores totais
    df_limpo = df_limpo.drop(df_limpo.index[[0,3]])

    # Criando dataframe unidirecional
    df_unidirecional = df_limpo.melt(id_vars=['tipo_veiculo', 'veiculo_especifico'], var_name='mes', value_name='quantidade')

    # Adicionando campos ao dataframe
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()
    return df_unidirecional

def licenciamento():
    df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[1], names=nomes_colunas)
    df_autoveic_novos_naci = criar_df_limpo(ini_linha=5, df=df_base, tipo_licenciamento='Autoveículos novos nacionais')
    df_autoveic_novos_import = criar_df_limpo(ini_linha=24, df=df_base, tipo_licenciamento='Autoveículos novos importados')
    df_total_autoveic_novos = criar_df_limpo(ini_linha=43, df=df_base, tipo_licenciamento='Total de autoveículos novos')
    df_resultado = pd.concat([df_autoveic_novos_naci, df_autoveic_novos_import, df_total_autoveic_novos])
    df_resultado.to_sql('anfavea_licenciamento', con=engine, schema=schema, if_exists=acao_insercao,index_label='id_licenciamento')