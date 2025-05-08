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

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Quando empacotado
    except AttributeError:
        base_path = os.path.abspath(".")  # Quando em desenvolvimento
    return os.path.join(base_path, relative_path)

dotenv_path = resource_path('token.env')
load_dotenv(dotenv_path = dotenv_path)

token = os.getenv('token')

# Nome do executável principal
executavel = 'XLogs.exe'

url_zip = f'https://api.github.com/repos/Giomelox/XLogs/releases/tags/v0.0.1'

BASE_PATH = Path(sys.executable).parent

# Caminho absoluto para a pasta system_main (2 níveis acima de system_manager/dist)
SYSTEM_MAIN = (BASE_PATH / '..' / '..' / 'system_main').resolve()

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
    
    elif resposta.status_code == 429:
        print('Muitas requisições ao mesmo tempo. Aguarde um pouco antes de tentar novamente.\nO programa será aberto sem atualização.')
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
    extract_path = Path.cwd() / 'new_version' / 'system_main'
    zip_path = Path.cwd() / 'update.zip'

    if not extract_path.exists():
        print(f"Erro: Diretório de extração não encontrado: {extract_path}")
        return

    arquivos_para_atualizar = [
        f for f in extract_path.glob('*') 
        if f.is_file() and f.name != 'updater.exe'
    ]

    if not arquivos_para_atualizar:
        print("Nenhum arquivo encontrado para atualizar.")
        return

    print(f"\nIniciando substituição de {len(arquivos_para_atualizar)} arquivos...")

    for arquivo_origem in arquivos_para_atualizar:
        if arquivo_origem.name in ['usuario_autenticado.txt', 'Configurações de usuario.txt']:
            continue

        arquivo_destino = SYSTEM_MAIN / arquivo_origem.name

        try:
            print(f"Substituindo: {arquivo_origem.name}")
            
            if sys.platform == 'win32' and arquivo_destino.exists():
                subprocess.run(
                    ['taskkill', '/F', '/IM', arquivo_destino.name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(0.5)

            if arquivo_destino.exists():
                arquivo_destino.unlink()
            
            shutil.copy2(arquivo_origem, arquivo_destino)
            print(f"✓ {arquivo_origem.name} atualizado com sucesso")

        except Exception as e:
            print(f"✗ Falha ao atualizar {arquivo_origem.name}: {str(e)}")

    shutil.rmtree(extract_path.parent)
    zip_path.unlink(missing_ok=True)

    with open(VERSAO_JSON_PATH, 'w', encoding = 'utf-8') as f:
        json.dump({
            'versao': str(nova_versao),
            'url': str(url_zip)
        }, f, ensure_ascii = False, indent = 4)

    print("\nAtualização de arquivos concluída.")

def relancar_app():
    base_path = Path(sys.executable).parent
    caminho_app = (base_path / '..' / '..' / 'system_main' / 'XLogs.exe').resolve()
    
    if not caminho_app.exists():
        print(f'Erro: XLogs.exe não encontrado em: {caminho_app}')
        return

    print(f'Abrindo o aplicativo: {caminho_app}')
    subprocess.Popen([str(caminho_app)])
    sys.exit(0)  # encerra o updater

def main():
    versao_remota, url_remota = verificar_nova_versao()
    versao_local, _ = obter_versao_local(VERSAO_JSON_PATH)

    if versao_remota is None or url_remota is None:
        print('Não foi possível verificar a versão. Abrindo app normalmente.')
        relancar_app()
        return

    if versao_remota != versao_local:
        print(f'Nova versão disponível: {versao_remota} || local: {versao_local}')
        aguardar_fechamento()
        baixar_zip(url_remota)
        extrair_zip()
        substituir_arquivos(versao_remota, url_remota)
        relancar_app()
    else:
        print(f'Versão remota: {versao_remota} || Versão local: {versao_local}')
        print('Aplicativo já está na última versão.')
        relancar_app()

main()
