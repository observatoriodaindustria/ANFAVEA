import requests as rq
import os
import shutil
from valores_uteis import caminho_arquivo
import datetime as dt

def baixar_arquivo():
    ano_para_dowload = dt.datetime.now().year
    
    if not os.path.exists('Arquivo'):
        os.makedirs('Arquivo')
    else:
        shutil.rmtree('Arquivo')
        os.makedirs('Arquivo')

    try:
        url = f'https://anfavea.com.br/docs/siteautoveiculos{ano_para_dowload}.xlsx'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        resposta = rq.get(url, headers=headers)
        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
    except:
        ano_para_dowload-=1
        url = f'https://anfavea.com.br/docs/siteautoveiculos{ano_para_dowload}.xlsx'

        resposta = rq.get(url, headers=headers)
        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)

def ano_mais_recente_dados():
    ano_para_dowload = dt.datetime.now().year
    try:
        url = f'https://anfavea.com.br/docs/siteautoveiculos{ano_para_dowload}.xlsx'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        resposta = rq.get(url, headers=headers)
        if resposta.status_code == 200:
            return ano_para_dowload
        
    except:
        ano_para_dowload-=1
        url = f'https://anfavea.com.br/docs/siteautoveiculos{ano_para_dowload}.xlsx'
        resposta = rq.get(url, headers=headers)
        if resposta.status_code == 200:
            return ano_para_dowload

ano_atual = ano_mais_recente_dados()