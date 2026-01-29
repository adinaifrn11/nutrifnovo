#Configurando o banco
from flask import Flask, render_template, flash, redirect
from models import Usuario
#Inicializando o login_manager
from utils import db,lm
import os
#importando o migrate
from flask_migrate import Migrate
from models import Usuario

#Criando a aplicação
app = Flask(__name__)

#Lendo as variáveis do arquivo flaskenv
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

#Criando a string de conexão
conexao = "sqlite:///nutrif.db"

#Ligando o flask ao banco
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializando o banco
db.init_app(app)
#Inicializando o Login_Manager
lm.init_app(app)


#importando o migrate
migrate = Migrate(app, db)

#Rotas do CRUD

#Rota Create
@app.route("/create")
def create():
    u = Usuario("Maria", "maria@gmail.com", "123456")
    db.session.add(u)
    db.session.commit()
    return 'Dados inseridos com sucesso'

#Rota Select
@app.route("/select")
def select():
    u = Usuario.query.all()
    print(u)

    u = Usuario.query.get(1)
    return u.nome

#Rota Update
@app.route("/update")
def update():
    u = Usuario.query.get(1)
    u.nome = "Maria Moura"
    db.session.add(u)
    db.session.commit()
    return 'Dados atualizados com sucesso'

#Rota Delete
@app.route("/delete")
def delete():		
    u = Usuario.query.get(1)
    db.session.delete(u)
    db.session.commit()
    return 'Dados excluídos com sucesso'

#Página 'para acesso negado'
@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 401








