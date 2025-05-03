from app.funções.funções_Gerais import obter_usuarios_validos, navigate, resource_path
import flet as ft

def login(current_view, views, page):

    page.title = 'Matec'
    page.padding = 0  
    page.margin = 0 
    page.spacing = 0
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False 
    page.window.maximizable = False

    lista_autenticar = obter_usuarios_validos()

    def salvar_configs_entrar():
        email_autenticar = input_usuario.value

        with open('usuario_autenticado.txt', 'w') as f:
            # Escreve os dados no arquivo, separados por vírgulas
            f.write(f'{email_autenticar}')

    def carregar_configs_entrar():
        try:
            with open('usuario_autenticado.txt', 'r') as f:
                dados_entrar = f.read()
                
                dados_entrar = [item.strip() for item in dados_entrar.split(',')]

                # Atribui os valores lidos para os campos de texto
                input_usuario.value = dados_entrar[0]

        except FileNotFoundError:
            pass 
        except ValueError:
            pass 

    snackbar = ft.SnackBar(content = ft.Text(""))
    page.snack_bar = snackbar 
    page.add(snackbar) 
    page.update() 

    def mostrar_snackbar(mensagem, cor):
        """Atualiza e exibe o SnackBar."""

        snackbar.content.value = mensagem 
        snackbar.bgcolor = cor 
        snackbar.open = True
        page.update() 

    def validar_usuario(e):
        """Valida o e-mail do usuário."""   
        email = input_usuario.value.strip()
        
        if not email:  
            mostrar_snackbar('Por favor, insira um usuário.', ft.Colors.RED)
        elif email not in [u for u in lista_autenticar]:  
            mostrar_snackbar('Usuário inválido.', ft.Colors.RED)
        elif email in [u for u in lista_autenticar]:
            mostrar_snackbar('Usuário autenticado com sucesso.', ft.Colors.GREEN)
            navigate(current_view, page, views, 'Menu Principal')

            salvar_configs_entrar()

    imagem_logomarca = ft.Container(
        content = ft.Image(
            src = resource_path('imagens/logomarca.png'),
            fit = ft.ImageFit.CONTAIN,
            width = 50,
            height = 50,
        ),
        alignment = ft.alignment.top_left,
        margin = ft.margin.only(top = -120)
    )

    texto_boas_vindas = ft.Text(
            'Boas vindas!',
            color = 'white',
            weight = 'bold',
            size = 55,
            font_family = 'Times New Roman', # Courier New; Times New Roman; Georgia
    )

    divisória = ft.Container(
        content = ft.Divider(
            height = 1,
            thickness = 2,
            color = ft.Colors.WHITE,
        ),
        width = 220
    )

    texto_apresentação = ft.Text(
        'Este é o LogiFlow, seu sistema de automação para processos logísticos. Ganhe eficiência, agilidade e controle total das operações.',
        color = 'white',
        size = 20
    )

    quadrante_boas_vindas = ft.Container(
        content = ft.Column(
            controls = [
                imagem_logomarca,
                texto_boas_vindas, 
                divisória,
                texto_apresentação
                ],
            spacing = 50,
            alignment = ft.MainAxisAlignment.CENTER,
            width = 480,
        ),
        margin = ft.margin.only(bottom = 150, left = -10)
    )

    input_usuario = ft.TextField(
        label = 'Usuário',
        border_radius = 15,
        color = ft.Colors.BLACK,
        bgcolor = ft.Colors.WHITE,
        border_color = ft.Colors.BLACK,
        label_style = ft.TextStyle(color = ft.Colors.BLACK38),
        prefix_icon = ft.Icon(ft.Icons.PERSON_SHARP, color = '#5A0B38'),
        width = 400
    )

    botao_entrar = ft.TextButton(
        text = 'Entrar',
        style = ft.ButtonStyle(color = '#5A0B38', bgcolor = ft.Colors.WHITE, text_style = ft.TextStyle(size = 18)),
        width = 150,
        height = 50,
        on_click = validar_usuario
    )

    quadrante_principal = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text('Login', size = 30, weight = 'bold', color = ft.Colors.WHITE, text_align = ft.TextAlign.CENTER),
                input_usuario,
                ft.Divider(height = 1, thickness = 2, color = ft.Colors.WHITE),
                ft.Row(
                    controls = [
                        botao_entrar
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 50,
        ),
        border_radius = 20,
        padding = 20,
        width = 350,
        height = 400,
        blur = ft.Blur(10,10),
        alignment = ft.alignment.center,
    )

    carregar_configs_entrar()

    container_pai = ft.Container(
        content = ft.Stack(
            controls = [
                ft.Image(
                    src = resource_path('imagens/imagem_tela_login.png'),
                    width = float('inf'),
                    height = 800,
                    fit = ft.ImageFit.COVER
                ),
                ft.Container(
                    content = ft.Row(
                        controls = [quadrante_boas_vindas, quadrante_principal],
                        alignment = ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    alignment = ft.alignment.center,
                    expand = True,
                )
            ]
        ),
        expand = True,
        height = 800,
    )

    return container_pai
