#Configurando o banco
from flask import Flask, render_template, request, flash, redirect, url_for
from models import Usuario
#Inicializando o login_manager
from utils import db,lm
import os
#importando o migrate
from flask_migrate import Migrate
from models import Usuario
from flask_login import logout_user, login_required
from flask_login import login_user
from flask_login import current_user


#Criando a aplicação
app = Flask(__name__)


#Lendo as variáveis do arquivo flaskenv
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT') or 3308

#Criando a string de conexão
conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"


#Ligando o flask ao banco
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializando o banco
db.init_app(app)
#Inicializando o Login_Manager
lm.init_app(app)


#importando o migrate
migrate = Migrate(app, db)

#ROTAS

#pagina inicial
@app.route('/')
def index():
    return render_template('index.html')

#login

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        # procurar usuário no banco
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for("index"))

        flash("Email ou senha incorretos!")

    return render_template("login.html")
@lm.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/logoff')
@login_required
def logoff():
    logout_user()
    return redirect(url_for('index'))  # ou qualquer rota de destino

#cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        print("CHEGOU NO POST!")  # 👈 teste

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        print("Recebido:", nome, email, senha)

        novo_usuario = Usuario(nome, email, senha)

        db.session.add(novo_usuario)
        db.session.commit()

        print("SALVO NO BANCO!")  # 👈 teste

        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route('/perfilservidor')
def perfilservidor():
    return render_template('perfilservidor.html') 

@app.route('/perfilusuario')
def perfilusuario():
    return render_template('perfilusuario.html') 

#cardápio   
@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

#feedback
feedbacks_lista = []
@app.route("/feedback", methods=['POST'])
def feedback():
    msg = request.form.get('mensagem')
    feedbacks_lista.append(msg)
    return redirect(url_for("feedback_resultados"))

@app.route("/feedback_form")
def feedback_form():
    return render_template("feedback.html")

@app.route("/feedback_resultados")
def feedback_resultados():  # ✔ NOME ARRUMADO
    return render_template("feedback_resultados.html", mensagem=feedbacks_lista)  # ✔ RETURN adicionado

#receitas
@app.route('/receitas')
def receitas():
    return render_template('receitas.html') 

@app.route('/prato')
def prato():
    return render_template('prato.html') 

#contatos
@app.route('/contatos')
def contato():
    return render_template('contatos.html')   

#restricao
@app.route('/restricao')
def restricao():   
    return render_template('restricao.html')  

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

#rota delete funcional com o banco
@app.route("/excluir_conta", methods=["POST"])
@login_required
def excluir_conta():
    db.session.delete(current_user)
    db.session.commit()

    logout_user()
    flash("Conta excluída com sucesso.")
    return redirect(url_for("index"))

#Página 'para acesso negado'
@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 401

#voltar pagina 
@app.route("/voltar")
def voltar():
    return redirect(request.referrer or url_for("index"))

if __name__ == "__main__":    
    app.run()    








