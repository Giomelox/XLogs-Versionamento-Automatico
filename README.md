# XLogs

## Estrutura de arquivos para utilizar como executável.

### 1º: Estar na pasta do updater (pelo terminal) e utilizar (pyinstaller --onefile --add-data "token.env;." updater.py) para empacotar o executável do atualizador automático, lembre de deixar o arquivo token na mesma pasta do updater.

### 2º: Estar na pasta do XLogs (pelo terminal) e utilizar (pyinstaller --noconfirm --clean --onefile --windowed --add-data "app/imagens;imagens" --add-data "app/funções/credentials.json;." XLogs.py) para empacotar o executável do arquivo principal juntamente das imagens.

### 3º: Separar os arquivos .exe gerados em duas pastas, sejam elas: system_main (adicione à esta pasta, o XLogs.exe e a pasta contendo as imagens). 
### e a outra pasta que deve ser criada abaixo de system_main, é system_manager/dist (adicione à esta pasta, o versão.json e o updater.exe)

## Como começar a preparar atualização

### 1º: Faça as alterações necessárias no XLogs.py ou em suas dependências (imagens, caminhos relativos, alterações no app/screens etc.) e empacote utilizando -> pyinstaller --noconfirm --clean --onefile --windowed --add-data "app/imagens;imagens" --add-data "app/funções/credentials.json;." XLogs.py <- (não se esqueça de navegar até a pasta pelo terminal).

### 2º: Após criar o XLogs.exe, coloque-o em sua pasta system_main criada anteriormente, e então vá para a pasta 'system_manager/dist' e encontre versão.json, abra o arquivo .json e altere a versão (ex: 0.0.5).

### 3º: Após alterar a versão na pasta local e ter feito as mudanças necessárias para preparar a atualização, selecione as pastas (system_main e system_manager) e crie um arquivo zip delas.

### 4º: Vá até o github e altere a versão.json da branch MAIN para a mesma versão que colocou no .json da sua máquina (ex: 0.0.5).

### 5º: Vá para o releases do github e retire o arquivo .zip antigo que estava lá (ou altere o nome para manter salvo) e baixe o arquivo .zip criado com as atualizações (o nome precisa ser XLogs.zip).
