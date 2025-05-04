from flask import Flask, request, jsonify
from servidor.models import db, Usuario
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar as tabelas no primeiro acesso
@app.before_request
def criar_tabelas():
    db.create_all()

@app.route('/')
def home():
    return 'Servidor funcionando no Render!'

@app.route('/validar_usuario', methods = ['POST'])
def validar_usuario():
    dados = request.json
    email = dados.get('email')

    if not email:
        return jsonify({'erro': 'Email não encontrado'}), 400
    
    usuario = Usuario.query.get(email)

    if usuario:
        return jsonify({'autoizado': True})
    return jsonify({'autorizado': False})

@app.route('/usuarios', methods = ['GET'])
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify({'usuarios': [u.email for u in usuarios]})
    except Exception as e:
        return jsonify({'erro': f'Erro ao obter usuários: {str(e)}'}), 500
    
@app.route('/usuarios', methods = ['POST'])
def adicionar_usuario():
    dados = request.json
    email = dados.get('email')
    status = dados.get('status', 'valido')

    if not email:
        return jsonify({'erro': 'Email não fornecido'}), 400

    if Usuario.query.get(email):
        return jsonify({'erro': 'Usuário já existe'}), 409
    
    novo_usuario = Usuario(email = email, status = status)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': f'Usuário {email} adicionado com status {status}'})

@app.route('/usuarios', methods = ['DELETE'])
def remover_usuario():
    dados = request.json
    email = dados.get('email')

    if not email:
        return jsonify({'erro': 'Email não fornecido'}), 400

    usuario = Usuario.query.get(email)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'mensagem': f'Usuário {email} removido com sucesso'})
    else:
        return jsonify({'erro': f'Usuário {email} não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug = True)
