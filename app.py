from download_arquivo import baixar_arquivo

# Baixando arquivo
baixar_arquivo()

from licenciamento_motorizacao import licenciamento_motorizacao
from licenciamento_combustivel import licenciamento_combustivel
from licenciamento_empresas import licenciamento_empresas
from exportacao_volume import export_volume
from outras_informacoes import outras_info
from licenciamento import licenciamento
from producao import producao

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

# Iserindo valores de Exportação por Volume no banco
export_volume()

print("\n\nTabelas ANFAVEA inseridas com sucesso!\n\n")