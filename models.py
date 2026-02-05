#Preparando o model Usuario para autenticação
from utils import db
from flask_login import UserMixin

#Essa classe representa uma tabela do banco
#Cada atributo representa uma coluna
class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    tipo = db.Column(
        db.String(20),
        nullable=False,
        default="aluno"
    )
    # aluno ou nutricionista

    def __init__(self, nome, email, senha, tipo="aluno"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    

class Cardapio(db.Model):
    __tablename__ = "cardapio"

    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)
    refeicao = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Cardapio {self.dia_semana}>"


