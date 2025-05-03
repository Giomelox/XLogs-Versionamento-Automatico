from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    email = db.Column(db.String, primary_key = True)
    status = db.Column(db.String, default = 'valido')