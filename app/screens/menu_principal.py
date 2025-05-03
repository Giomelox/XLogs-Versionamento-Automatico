from app.funções.funções_Gerais import navigate, SolicitarPlanilha, resource_path
import flet as ft

def menu_principal(current_view, views, page):

    page.title = 'Matec'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 1300 
    page.window.height = 900
    page.window.resizable = False 
    page.window.maximizable = False

    solicitador = SolicitarPlanilha(page)

    botao_escolher_planilha = ft.ElevatedButton(
        color = ft.Colors.BLACK,
        bgcolor = ft.Colors.BLUE_400,
        width = 250,
        height = 60,
        on_click = solicitador.abrir_seletor,
        content = ft.Container(
            content = ft.Row(
            alignment = ft.MainAxisAlignment.START,
            controls = [
                ft.Container(
                    content = ft.Icon(ft.icons.CHANGE_CIRCLE, color = ft.Colors.BLACK87), margin = ft.margin.only(left = 30)),

                ft.Container(
                    content= ft.Text('Escolher planilha'))
                ],
                spacing = 15,
            ),
        ),
    )

    botao_recebimento = ft.Container(
        content = ft.ElevatedButton(
            color = ft.Colors.BLACK,
            bgcolor = ft.Colors.BLUE_200,
            width = 250,
            height = 60,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Recebimento de peças'),
            content = ft.Container(
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    controls = [
                        ft.Container(
                            content = ft.Icon(ft.icons.ARCHIVE, color = ft.Colors.BLACK87), margin = ft.margin.only(left = 30)),

                        ft.Container(
                            content = ft.Text('Recebimento de peças', color = 'black'))
                    ],
                    spacing = 15,
                ),
            ),
        ),
    )

    botao_devolução = ft.Container(
        content = ft.ElevatedButton(
            color = ft.Colors.BLACK,
            bgcolor = ft.Colors.BLUE_300,
            width = 250,
            height = 60,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Devolução de peças'),
            content = ft.Container(
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    controls = [
                        ft.Container(
                            content = ft.Icon(ft.icons.UNARCHIVE, color = ft.Colors.BLACK87), margin = ft.margin.only(left = 30)),

                        ft.Container(
                            content = ft.Text('Devolução de peças', color = 'black'))
                    ],
                    spacing = 15,
                ),
            ), 
            
        )
    )

    botao_difal = ft.Container(
        content = ft.ElevatedButton(
            color = ft.Colors.BLACK,
            bgcolor = ft.Colors.BLUE_400,
            width = 250,
            height = 60,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Difal'),
            content = ft.Container(
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    controls = [
                        ft.Container(
                            content = ft.Icon(ft.icons.CALCULATE, color = ft.Colors.BLACK87), margin = ft.margin.only(left = 30)),

                        ft.Container(
                            content = ft.Text('Planilha Difal Mensal', color = 'black'))
                    ],
                    spacing = 15,
                ),
            ),       
        )
    )

    botao_configurações = ft.Container( 
        content = ft.ElevatedButton(
            color = ft.colors.BLACK,
            bgcolor = ft.colors.WHITE, 
            width = 250,
            height = 60,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Configurações'),
            content = ft.Container(
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    controls = [
                        ft.Container(
                            content = ft.Icon(ft.icons.SETTINGS, color = ft.Colors.BLACK87), margin = ft.margin.only(left = 30)),

                        ft.Container(
                            content = ft.Text('Configurações', color = 'black'))
                    ],
                    spacing = 30,
                ),
            )
        ),
        margin = ft.margin.only(bottom = 200, left = 650)
    )

    container_botoes = ft.Container(
        content = ft.Column(
            controls = [botao_escolher_planilha, botao_recebimento, botao_devolução, botao_difal],
            spacing = 20,
            
        ),
        margin = ft.margin.only(top = 110, left = 650),
        alignment = ft.alignment.center_right,
    )

    container_pai = ft.Container(
        content = ft.Stack(
            controls = [
                ft.Image(
                    src = resource_path('imagens/imagem_tela_login.png'),
                    width = float('inf'),
                    height = 800,
                    fit = ft.ImageFit.COVER
                ),

                ft.Column(
                    controls = [
                        ft.Container(
                            content = ft.Row(
                                controls = [container_botoes],
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                        ),

                        ft.Container(
                            content = ft.Row(
                                controls = [botao_configurações],
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                        )
                    ],
                    spacing = 180,
                )
            ]
        ),
        height = 800,
    )

    return container_pai
