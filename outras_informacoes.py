import pandas as pd
import datetime as dt
from valores_uteis import caminho_arquivo, nomes_planilhas, engine, schema, acao_insercao
from download_arquivo import ano_atual


nomes_colunas = ['nada', 'tipo_veiculo', 'veiculo_especifico', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']
df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[7], names=nomes_colunas)

def criar_df_limpo_desmontados(df=df_base):
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:5])
    df_limpo = df_limpo.drop(df_limpo.index[9:]).reset_index(drop=True)
    df_limpo.loc[1:3,'tipo_veiculo'] = 'Veículos leves'
    df_limpo = df_limpo.drop(df_limpo.index[:2]).reset_index(drop=True)
    df_limpo = df_limpo.drop(df_limpo.index[4:])
    df_limpo.loc[2,'veiculo_especifico'] = 'Caminhões'
    df_limpo.loc[3,'veiculo_especifico'] = 'Ônibus'

    # Deixando dados de maneira udnidimensional
    df_unidirecional = df_limpo.melt(id_vars=['tipo_veiculo', 'veiculo_especifico'], var_name='mes', value_name='quantidade')
    
    # Adicionando campos ao dataframe
    df_unidirecional['tipo'] = 'Exportações de autoveículos desmontados (CKDs)'
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()
    
    # Enviando dados para o banco
    df_unidirecional.to_sql('anfavea_exp_veic_desmon', index_label='id_expo_veic_desmon', con=engine, if_exists=acao_insercao, schema=schema)


def export_setor_autovei(df=df_base):
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1]).drop(columns=nomes_colunas[2])
    df_limpo = df_limpo.drop(df_limpo.index[:19])
    df_limpo = df_limpo.drop(df_limpo.index[1:])
    df_limpo.rename(columns={'tipo_veiculo':'unidades'}, inplace=True)
    
    # Deixando dados de maneira udnidimensional
    df_unidirecional = df_limpo.melt(id_vars='unidades', var_name='mes', value_name='quantidade')

    # Adicionando campos ao dataframe
    df_unidirecional['tipo'] = 'Exportações em valor do setor de autoveículos'
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()
    
    # Enviando dados para o banco
    df_unidirecional.to_sql('anfavea_exp_setor_autovei', index_label='id_setor_autovei', schema=schema, con=engine, if_exists=acao_insercao)


def emprego_setor_autovei(df=df_base):
    # Limpando dados
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1]).drop(columns=nomes_colunas[2])
    df_limpo = df_limpo.drop(df_limpo.index[:28])
    df_limpo = df_limpo.drop(df_limpo.index[1:])
    df_limpo.rename(columns={'tipo_veiculo':'unidades'}, inplace=True)
    
    # Deixando dados de maneira udnidimensional
    df_unidirecional = df_limpo.melt(id_vars='unidades', var_name='mes', value_name='quantidade')

    # Adicionando campos ao dataframe
    df_unidirecional['tipo'] = 'Emprego no setor de autoveículos'
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()
    
    # Enviando dados para o banco
    df_unidirecional.to_sql('anfavea_emprego_setor_autovei', index_label='id_setor_autovei', schema=schema, if_exists=acao_insercao, con=engine)

def outras_info():
    criar_df_limpo_desmontados()
    export_setor_autovei()
    emprego_setor_autovei()