import os
import sys
import time
import json
import zipfile
import shutil
import requests
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path = os.path.join(os.getcwd(), 'token.env'))
token = os.getenv('token')

# Nome do executável principal
executavel = 'XLogs.exe'

url_zip = f'https://api.github.com/repos/Giomelox/XLogs/releases/tags/v0.0.1'

BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)).resolve()

# Caminho absoluto até system_main
SYSTEM_MAIN = BASE_DIR.parent.parent / 'system_main'

# Caminho até o token.env
DOTENV_PATH = 'token.env'

# Caminho até a versão.json no mesmo nível de system_main e system_manager
VERSAO_JSON_PATH = 'versão.json'

def verificar_nova_versao():
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.raw',
        'User-Agent': 'Mozilla/5.0'
    }

    url_remoto = 'https://raw.githubusercontent.com/Giomelox/XLogs/refs/heads/main/versao.json'
    resposta = requests.get(url_remoto, headers = headers)

    if resposta.status_code == 200:
        try:
            dados_remoto = resposta.json()
            versao_remota = dados_remoto['versao']  # Pega a versão apenas, sem o URL
            url_download = dados_remoto['url']  # Pega o URL
            return versao_remota, url_download
        except ValueError as e:
            print(f"Erro ao tentar converter a resposta em JSON: {e}")
            print("Conteúdo retornado:", resposta.text)  # Exibe o conteúdo da resposta
            return None, None
    else:
        print(f"Erro ao obter versão remota. Status: {resposta.status_code}")
        print("Conteúdo retornado:", resposta.text)  # Exibe o conteúdo da resposta em caso de erro
        return None, None

def obter_versao_local(caminho_versao_json):
    if not os.path.exists(caminho_versao_json):
        return None

    with open(caminho_versao_json, 'r', encoding = 'utf-8') as f:
        dados_local = json.load(f)
        versao_local = dados_local['versao']
        url_download_local = dados_local['url']
        return versao_local, url_download_local

def aguardar_fechamento():
    while True:
        result = subprocess.run(f"tasklist /FI 'IMAGENAME eq {executavel}'", capture_output = True, text = True)
        if executavel not in result.stdout:
            break
        time.sleep(1)

def baixar_zip(url_zip):

    asset_name = 'XLogs.zip'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url_zip, headers = headers)

    if response.status_code == 404:
        print('Não deu certo')
        sys.exit(1)

    elif response.status_code != 200:
        print('Funcionou')
        sys.exit(1)

    release_data = response.json()

    assets = release_data.get('assets', [])

    # Procurar o asset pelo nome
    asset = next((a for a in assets if a.get('name')  ==  asset_name), None)
    if asset is None:
        sys.exit(1)

    asset_id = asset.get('id')
    
    # 2. Requisição para baixar o asset
    download_url = f'https://api.github.com/repos/Giomelox/XLogs/releases/assets/{asset_id}'

    download_headers = {
        'Accept': 'application/octet-stream',
        'Authorization': f'Bearer {token}'
    }

    dl_response = requests.get(download_url, headers = download_headers, stream = True)

    if dl_response.status_code  ==  404:
        sys.exit(1)

    elif dl_response.status_code in (401, 403):
        sys.exit(1)

    elif dl_response.status_code !=  200:
        sys.exit(1)

    # 3. Salvar o conteúdo do asset em 'update.zip'
    with open('update.zip', 'wb') as f:
        for chunk in dl_response.iter_content(chunk_size = 8192):
            if chunk:
                f.write(chunk)

def extrair_zip():
    zip_path = Path.cwd() / 'update.zip'
    extract_path = Path.cwd() / 'new_version'

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if not extract_path.exists():
            extract_path.mkdir()
        zip_ref.extractall(extract_path)
    print('Conteúdo extraído:', os.listdir(extract_path))

def substituir_arquivos(nova_versao, url_zip):
    extract_path = Path.cwd() / 'new_version'
    zip_path = Path.cwd() / 'update.zip'

    arquivos_extraidos = os.listdir(extract_path)
    
    for item in arquivos_extraidos:
        if item == 'updater.exe':
            continue

        src = extract_path / item
        dst = SYSTEM_MAIN / item

        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            if dst.exists():
                dst.unlink()
            shutil.copy2(src, dst)

    shutil.rmtree(extract_path)
    zip_path.unlink()

    with open(VERSAO_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({'versao': nova_versao, 'url': url_zip}, f, ensure_ascii=False, indent=4)

    print('Substituição concluída.')

def relancar_app():
    caminho_app = Path('..') / Path('..') / 'system_main' / 'XLogs.exe'
    caminho_app = caminho_app.resolve()
    
    if not caminho_app.exists():
        print(f'Erro: XLogs.exe não encontrado em: {caminho_app}')
        return

    print(f'Abrindo o aplicativo: {caminho_app}')
    subprocess.Popen([str(caminho_app)])
    sys.exit(0)  # encerra o updater

def main():
    versao_remota = verificar_nova_versao()
    versao_local = obter_versao_local(VERSAO_JSON_PATH)

    if versao_remota is None or url_zip is None:
        print('Não foi possível verificar a versão. Abrindo app normalmente.')
        relancar_app()
        return

    if versao_remota != versao_local:
        print(f'Nova versão disponível: {versao_remota} || local: {versao_local}')
        aguardar_fechamento()
        baixar_zip(url_zip)
        extrair_zip()
        substituir_arquivos(versao_remota, url_zip)
        relancar_app()
    else:
        print('Aplicativo já está na última versão.')
        relancar_app()

main()