from download_arquivo import baixar_arquivo, ano_atual

# Baixando arquivo
baixar_arquivo()

from licenciamento_motorizacao import licenciamento_motorizacao
from licenciamento_combustivel import licenciamento_combustivel
from licenciamento_empresas import licenciamento_empresas
from exportacao_volume import export_volume
from outras_informacoes import outras_info
from licenciamento import licenciamento
from producao import producao
from sqlalchemy import text
from valores_uteis import *

# Criando conexão com o banco:
conexao_banco = engine.connect()

# Removendo dados do ano mais recente para atualizar a inserção
tabelas = ['[anfavea_licenciamento]', '[anfavea_lic_empre]', '[anfavea_lic_motorizacao]',
           '[anfavea_exp_veic_desmon]', '[anfavea_exp_setor_autovei]', '[anfavea_lic_combus]',
           '[anfavea_producao]', '[anfavea_export_vol]','[anfavea_emprego_setor_autovei]']

for tabela in tabelas:
    conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].{tabela} WHERE ano = {ano_atual}"))

# Encerrando conexão com o banco
conexao_banco.close()

# Tratando e inserindo valores de Licenciamento no banco
licenciamento()

# Tratando e inserindo valores de Licenciamento empresas no banco
licenciamento_empresas()

# Tratando e inserindo valores de Licenciamento Motorização no banco
licenciamento_motorizacao()

# Tratando e inserindo valores de Licenciamento Combustível no banco
licenciamento_combustivel()

# Inserindo valores de Informações no banco
outras_info()

# Inserindo Produção no banco
producao()

# Iserindo valores de Exportação por Volume no banc
export_volume()


# Inserindo valores de Empregos no setor de Autoveículos
print("\n\nTabelas ANFAVEA inseridas com sucesso!\n\n")