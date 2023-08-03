from download_arquivo import baixar_arquivo, ano_atual

# Baixando arquivo
ano_atual = baixar_arquivo()

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

# Tratando e inserindo valores de Licenciamento no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_licenciamento] WHERE ano = {ano_atual}"))
conexao_banco.commit()
licenciamento()

# Tratando e inserindo valores de Licenciamento empresas no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_lic_empre] WHERE ano = {ano_atual}"))
licenciamento_empresas()

# Tratando e inserindo valores de Licenciamento Motorização no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_lic_motorizacao] WHERE ano = {ano_atual}"))
conexao_banco.commit()
licenciamento_motorizacao()

# Tratando e inserindo valores de Licenciamento Combustível no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_lic_combus] WHERE ano = {ano_atual}"))
conexao_banco.commit()
licenciamento_combustivel()

# Inserindo valores de Informações no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_exp_veic_desmon] WHERE ano = {ano_atual}"))
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_exp_setor_autovei] WHERE ano = {ano_atual}"))
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_emprego_setor_autovei] WHERE ano = {ano_atual}"))
conexao_banco.commit()
outras_info()

# Inserindo Produção no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_producao] WHERE ano = {ano_atual}"))
conexao_banco.commit()
producao()

# Iserindo valores de Exportação por Volume no banco
conexao_banco.execute(text(f"DELETE FROM [BD_OBSERVATORIO].[st].[anfavea_export_vol] WHERE ano = {ano_atual}"))
conexao_banco.commit()
export_volume()

# Encerrando conexão com o banco
conexao_banco.close()

print("\n\nTabelas ANFAVEA inseridas com sucesso!\n\n")