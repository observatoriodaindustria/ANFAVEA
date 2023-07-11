import requests as rq
import os
import shutil
from valores_uteis import caminho_arquivo

def baixar_arquivo():
    if not os.path.exists('Arquivo'):
        os.makedirs('Arquivo')
    else:
        shutil.rmtree('Arquivo')
        os.makedirs('Arquivo')

    url = 'https://anfavea.com.br/docs/siteautoveiculos2023.xlsx'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    resposta = rq.get(url, headers=headers)
    with open(caminho_arquivo, 'wb') as arquivo:
        arquivo.write(resposta.content)