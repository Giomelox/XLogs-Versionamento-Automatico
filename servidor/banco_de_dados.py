from models import db, Usuario
from flask import Flask
import os

'''OBS: ESTE CÓDIGO É VÁLIDO APENAS PARA USO LOCAL, PARA CRIAR, REMOVER, VALIDAR OU INVALIDAR ALGUM USUÁRIO DO BANCO DE DADOS.
NÃO COMPARTILHAR NEM PUBLICAR, POIS ESTÁ COM CHAVES PRIVADAS.'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:tgJj7yCsNTHv3wC0z0wwikT6AqoF5Aaq@dpg-d0b8p86uk2gs73cgge70-a.oregon-postgres.render.com/usuarios_yllo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def visualizar_tabela():
    with app.app_context():
        usuarios = Usuario.query.all()
    if not usuarios:
        print('Nenhum usuário encontrado.')
    else:
        for u in usuarios:
            print(f"\nEmail: {u.email}\n")

def criar_usuario(email):
    with app.app_context():
        # Verifica se o usuário já existe
        if Usuario.query.filter_by(email = email).first():
            print(f"Usuário '{email}' já existe.")
            return

        novo_usuario = Usuario(email = email)
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"Usuário '{email}' adicionado com sucesso.")

def remover_usuario(email):
    with app.app_context():
        # Verifica se o usuário existe no banco de dados
        usuario = Usuario.query.filter_by(email = email).first()
        
        if not usuario:
            print(f"Usuário '{email}' não encontrado.")
            return
        db.session.expunge(usuario)
        db.session.delete(usuario)  

        db.session.commit()
        print(f"Usuário '{email}' excluído com sucesso.")

if __name__ == '__main__':
    visualizar_tabela()
    #criar_usuario(email = 'matecrecifepe@gmail.com')
    #remover_usuario(email = 'matecrecifepe@gmail.com')
