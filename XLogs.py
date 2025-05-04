from dotenv import load_dotenv
import subprocess
import requests
import json
import sys
import os

load_dotenv(dotenv_path = os.path.join(os.getcwd(), 'token.env'))
token = os.getenv('token')

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3.raw',
    'User-Agent': 'Mozilla/5.0'
}

def verificar_nova_versao():
    # URL para acessar o arquivo 'versao.json' da branch main
    url = 'https://raw.githubusercontent.com/Giomelox/XLogs/main/versão.json'
    resposta = requests.get(url, headers=headers)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        nova_versao = dados['versao']
        return dados['url'], nova_versao
    else:
        print(f"Erro ao obter versão remota. Status: {resposta.status_code}")
    return None, None

# Função para ler a versão local do arquivo 'versao_local.json'
def ler_versao_local():
    caminho_versao = 'versão.json'
    if os.path.exists(caminho_versao):
        with open(caminho_versao, 'r') as f:
            dados = json.load(f)
            return dados.get('versao', None)
    return None

# Função para atualizar a versão local no arquivo 'versao_local.json'
def atualizar_versao_local(nova_versao):
    caminho_versao = 'versão.json'
    with open(caminho_versao, 'w') as f:
        json.dump({'versao': nova_versao}, f)

# Versão atual do app, lida do arquivo 'versao_local.json'
VERSAO_ATUAL = ler_versao_local()

if not VERSAO_ATUAL:
    print('Erro: versão atual não encontrada.')
    sys.exit()

# Verifica se há uma nova versão disponível
url_zip, nova_versao = verificar_nova_versao()

if url_zip:
    print(f'Versão local: {VERSAO_ATUAL}.\nNova versão disponível: {nova_versao}.')
    if nova_versao != VERSAO_ATUAL:
        print(f'Nova versão {nova_versao} disponível!')
        # Chama updater.exe e passa a URL do zip
        diretorio_atualizador = os.path.join(os.getcwd(), 'system_manager', 'dist', 'atualizador', 'atualizador.exe')
        subprocess.Popen([diretorio_atualizador, url_zip, nova_versao])
        
        # Atualiza a versão local para a nova versão
        atualizar_versao_local(nova_versao)
        
        sys.exit()
    else:
        print('Você já está com a versão mais recente.')
else:
    print('Erro: Não foi possível obter a versão remota.')

import app.app as app
app
