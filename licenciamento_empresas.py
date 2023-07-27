import pandas as pd
import datetime as dt
from valores_uteis import  caminho_arquivo, nomes_planilhas, engine, schema, acao_insercao
from download_arquivo import ano_atual

# Nomes respectivos das colunas das tabelas
nomes_colunas = ['nada', 'tipo_veiculo', 'veiculo_especifico','marca_veiculo', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

# Criando um Data Frame base
df_base = pd.read_excel(caminho_arquivo, sheet_name=nomes_planilhas[4], names=nomes_colunas)

# Definindo índices da tabelas
indice_automo   = df_base['tipo_veiculo'].to_list().index('Automóveis')
indice_cm_leve  = df_base['tipo_veiculo'].to_list().index('Comerciais leves') 
indice_caminhao = df_base['tipo_veiculo'].to_list().index('Caminhões')
indice_automo   = df_base['tipo_veiculo'].to_list().index('Automóveis') 
indice_camin_tot_empr = df_base['tipo_veiculo'].to_list().index('Caminhões - Total por empresa')
indice_onibus = df_base['tipo_veiculo'].to_list().index('Ônibus (chassi)')
indice_onibus_fim = num_linhas = df_base.shape[0]

# Função para limpar tabelas da maior parte dos automoveis
def criar_df_limpo_empre(ini_tabela=0, tam_tabela=0, df=df_base,tipo_veiculo = 'Automóveis',veiculo_especifico='Automovel',tipo_licenciamento='Licenciamento total de autoveículos leves por empresa'):

    # Definfinindo a tabela
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_tabela])
    df_limpo = df_limpo.drop(df_limpo.index[tam_tabela:]).reset_index(drop=True)
    df_limpo['associado_anfavea'] = ''

    # Renomeando alguns elementos da coluna 'veiculo_especifico'
    df_limpo.loc[2:tam_tabela,'tipo_veiculo'] = tipo_veiculo

    # Definindo alguns índices
    indice_anfa = df_limpo['veiculo_especifico'].to_list().index('Empresas associadas à Anfavea')
    fim_indice_anfa = df_limpo['veiculo_especifico'].to_list().index('Outras empresas')-1

    df_limpo.loc[indice_anfa:fim_indice_anfa,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[fim_indice_anfa+1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[2:,'veiculo_especifico'] = veiculo_especifico
    df_limpo.loc[fim_indice_anfa+1,'marca_veiculo'] = 'Veículos de outras empresas'
    df_limpo = df_limpo.drop(df_limpo.index[:2])

    # Criando tabela unidirecional e adicionando variaveis
    df_unidirecional = df_limpo.melt(id_vars=['tipo_veiculo', 'veiculo_especifico','marca_veiculo','associado_anfavea'], var_name='mes', value_name='quantidade')
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()

    # Retornando Data Frame
    return df_unidirecional


# Função para limpar apenas as tabelas de caminhões
def criar_df_limpo_empre_caminhoes(ini_tabela=0, tam_tabela=0, df=df_base,tipo_veiculo='Caminhões',tipo_licenciamento='Licenciamento total de autoveículos leves por empresa'):

    # Definfinindo a tabela
    df_limpo = df.drop(columns=nomes_colunas[:1]).drop(columns=nomes_colunas[-1])
    df_limpo = df_limpo.drop(df_limpo.index[:ini_tabela])
    df_limpo = df_limpo.drop(df_limpo.index[tam_tabela:]).reset_index(drop=True)
    df_limpo['associado_anfavea'] = ''

    # Resentando os índices
    df_limpo = df_limpo.reset_index(drop=True)
    
    # Encontrando índices de alguns elementos para medir distância entre eles
    indice_semileve = df_limpo['veiculo_especifico'].to_list().index('Semileves')
    indice_leve = df_limpo['veiculo_especifico'].to_list().index('Leves')
    indice_medio = df_limpo['veiculo_especifico'].to_list().index('Médios')
    indice_semipesados = df_limpo['veiculo_especifico'].to_list().index('Semipesados')
    indice_pesados = df_limpo['veiculo_especifico'].to_list().index('Pesados')
    indice_camin_tot_empr2 = df_limpo['tipo_veiculo'].to_list().index('Caminhões - Total por empresa')

    # Definindo todos os valores como caminhão
    df_limpo.loc[2:tam_tabela,'tipo_veiculo'] = tipo_veiculo

    # Renomeando alguns elementos daS colunas
    df_limpo.loc[indice_semileve:indice_leve-2,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[indice_leve-1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[indice_semileve:indice_leve-1,'veiculo_especifico'] = 'Semileves'

    # Renomeando alguns elementos daS colunas
    df_limpo.loc[indice_leve:indice_medio-2,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[indice_medio-1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[indice_leve:indice_medio-1,'veiculo_especifico'] = 'Leves'

    # Renomeando alguns elementos daS colunas
    df_limpo.loc[indice_medio:indice_semipesados-2,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[indice_semipesados-1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[indice_medio:indice_semipesados-1,'veiculo_especifico'] = 'Leves'

    # Renomeando alguns elementos daS colunas
    df_limpo.loc[indice_semipesados:indice_pesados-2,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[indice_pesados-1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[indice_semipesados:indice_pesados-1,'veiculo_especifico'] = 'Semipesados'

    # Renomeando alguns elementos daS colunas
    df_limpo.loc[indice_pesados:indice_camin_tot_empr2-2,'associado_anfavea'] = 'Empresa associada à Anfavea'
    df_limpo.loc[indice_camin_tot_empr2-1,'associado_anfavea'] = 'Empresa não associada à Anfavea'
    df_limpo.loc[indice_pesados:indice_camin_tot_empr2,'veiculo_especifico'] = 'Pesados'

    # Renomeando alguns elementos daS colunas
    indices_exclusao = [0,1,2,indice_leve,indice_leve+1,indice_medio,indice_medio+1,indice_semipesados,indice_semipesados+1,indice_pesados,indice_pesados+1,-1,-2]
    df_limpo = df_limpo.drop(df_limpo.index[indices_exclusao])

    # Adicionando campos específicos nas marcas de veículos que não são ANFAVEA
    df_limpo.loc[indice_leve-1,'marca_veiculo'] = 'Veículos de outras empresas'
    df_limpo.loc[indice_medio-1,'marca_veiculo'] = 'Veículos de outras empresas'
    df_limpo.loc[indice_semipesados-1,'marca_veiculo'] = 'Veículos de outras empresas'
    df_limpo.loc[indice_pesados-1,'marca_veiculo'] = 'Veículos de outras empresas'
    df_limpo.loc[indice_camin_tot_empr2-1,'marca_veiculo'] = 'Veículos de outras empresas'

    # Resetando os índices
    df_limpo = df_limpo.reset_index(drop=True)
    
    # Criando tabela unidirecional e adicionando variaveis
    df_unidirecional = df_limpo.melt(id_vars=['tipo_veiculo', 'veiculo_especifico','marca_veiculo','associado_anfavea'], var_name='mes', value_name='quantidade')
    df_unidirecional['tipo_licenciamento'] = tipo_licenciamento
    df_unidirecional['ano'] = ano_atual
    df_unidirecional['dt_carga'] = dt.datetime.now()
    return df_unidirecional


def licenciamento_empresas():
    
    # Execuatando função
    df_automoveis = criar_df_limpo_empre(ini_tabela=indice_automo, tam_tabela=(indice_cm_leve - indice_automo), tipo_licenciamento='Licenciamento total de autoveículos leves por empresa')
    df_comerciasi_leves = criar_df_limpo_empre(ini_tabela=indice_cm_leve, veiculo_especifico='Comerciais leves',tam_tabela=(indice_caminhao-indice_cm_leve))
    df_onibus = criar_df_limpo_empre(ini_tabela=indice_onibus, veiculo_especifico='Ônibus',tipo_veiculo='Ônibus (chassi)',tam_tabela=(indice_onibus_fim-indice_onibus))
    df_caminhoes = criar_df_limpo_empre_caminhoes(ini_tabela=indice_caminhao, tam_tabela=(indice_camin_tot_empr-indice_caminhao)+2, tipo_veiculo='Caminhões')

    # Juntando as tabelas
    df_resultado = pd.concat([df_automoveis,df_comerciasi_leves, df_onibus, df_caminhoes]).reset_index(drop=True)

    # Enviando para o banco
    df_resultado.to_sql('anfavea_lic_empre', schema=schema, if_exists=acao_insercao, index_label='id_empresas',con=engine)