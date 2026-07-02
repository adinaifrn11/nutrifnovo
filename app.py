# ============================
# app.py - versão original do usuário
# ============================
from flask import session
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, Cardapio  # Ajuste conforme seus modelos
from utils import db, lm
import os
import requests
from config import Config
from authlib.integrations.flask_client import OAuth
# ============================
# Criando a aplicação
# ============================
app = Flask(__name__)
app.config.from_object(Config)

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

print("SECRET_KEY:", repr(app.config["SECRET_KEY"]))
print("CLIENT_ID:", repr(app.config["SUAP_CLIENT_ID"]))


# Configuração do banco
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT') or 3308

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando banco e login
db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)
lm.login_view = "login"

# ============================
# User loader
# ============================
@lm.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ============================
# Rotas
# ============================

# Página inicial pública (redireciona para login)
@app.route('/')
def index():
    return render_template('index.html')

oauth = OAuth(app)

oauth.register(
    name="suap",
    client_id=app.config["SUAP_CLIENT_ID"],
    client_secret=app.config["SUAP_CLIENT_SECRET"],
    authorize_url="https://suap.ifrn.edu.br/o/authorize/",
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    api_base_url="https://suap.ifrn.edu.br/api/",
    client_kwargs={
        "scope": "identificacao"
    },
    client_auth_method="client_secret_post"
)

@app.route('/index2')
@login_required
def index2():
    return render_template('index2.html')

# Login
from flask import request
from flask import session

@app.route("/login/suap")
def login_suap():

    session["teste"] = "ok"

    print("SESSION LOGIN:", dict(session))

    redirect_uri = url_for("callback_suap", _external=True)

    return oauth.suap.authorize_redirect(redirect_uri)


@app.route("/authorize/suap")
def callback_suap():

    print("SESSION:", dict(session))
    print("COOKIES:", request.cookies)
    print("ARGS:", request.args)

    token = oauth.suap.authorize_access_token()

    # Busca os dados do usuário no SUAP.
    # A API foi atualizada e o endpoint mudou de lugar, então tentamos
    # os possíveis endpoints em ordem até algum retornar JSON válido.
    endpoints = [
        "eu/",
        "rh/eu/",
        "ensino/meus-dados-aluno/",
        "rh/meus-dados/",
    ]

    dados = None
    for ep in endpoints:
        resp = oauth.suap.get(ep, token=token)
        ctype = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "application/json" in ctype:
            dados = resp.json()
            print("SUAP OK via endpoint:", ep, "->", dados)
            break
        else:
            print("Tentativa falhou:", ep, resp.status_code, ctype)

    if dados is None:
        print("Nenhum endpoint do SUAP retornou dados válidos.")
        abort(502)

    matricula = dados.get("matricula") or dados.get("identificacao")
    nome = (
        dados.get("nome_usual")
        or dados.get("nome_registro")
        or dados.get("nome")
        or matricula
    )
    email = (
        dados.get("email")
        or dados.get("email_google_classroom")
        or dados.get("email_academico")
        or dados.get("email_secundario")
        or f"{matricula}@suap.ifrn.edu.br"
    )

    # Procura o usuário pelo email; se não existir, cria um novo
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario is None:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha="",  # login via SUAP não usa senha local
            tipo="aluno",
        )
        db.session.add(usuario)
        db.session.commit()

    login_user(usuario)
    return redirect(url_for("index2"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"] # Aqui a variável se chama 'senha'
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        # 1. Verifica se o usuário existe
        # 2. Compara a senha do banco com a senha que veio do formulário
        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for("index2"))
        else:
            flash("Email ou senha incorretos!")

    return render_template("login.html")

# Logout
@app.route('/logoff')
@login_required
def logoff():
    logout_user()
    flash("Você saiu da conta.")
    return redirect(url_for('login'))

#
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # 🔎 VERIFICA SE EMAIL JÁ EXISTE
        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash("Esse email já está cadastrado!")
            return redirect(url_for("cadastro"))

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            tipo="aluno"
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for("login"))

    return render_template("cadastro.html")
# ============================
# Páginas protegidas
# ============================
@app.route('/perfilusuario')
@login_required
def perfilusuario():
    return render_template('perfilusuario.html')

@app.route('/perfilservidor')
@login_required
def perfilservidor():
    return render_template('perfilservidor.html')
    
@app.route('/cardapioRefeicoes')
def cardapioRefeicoes():
    return render_template('cardapioRefeicoes.html')

@app.route('/cardapioLanche') 
def cardapioLanche(): 
    return render_template('cardapioLanche.html')

@app.route('/cardapio')
@login_required
def cardapio():
    return render_template('cardapio.html')

@app.route("/cardapio/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cardapio(id):
    if current_user.tipo != "nutricionista":
        abort(403)

    cardapio = Cardapio.query.get_or_404(id)

    if request.method == "POST":
        cardapio.dia_semana = request.form["dia_semana"]
        cardapio.refeicao = request.form["refeicao"]
        db.session.commit()
        return redirect(url_for("cardapio"))

    return render_template("editar_cardapio.html", cardapio=cardapio)

# Feedback
feedbacks_lista = []

@app.route("/feedback_form")
@login_required
def feedback_form():
    return render_template("feedback.html")

@app.route("/feedback", methods=['POST'])
@login_required
def feedback():
    msg = request.form.get('mensagem')
    feedbacks_lista.append(msg)
    return redirect(url_for("feedback_resultados"))

@app.route("/feedback_resultados")
@login_required
def feedback_resultados():
    return render_template("feedback_resultados.html", mensagem=feedbacks_lista)

# Receitas
@app.route('/receitas')
def receitas():
    return render_template('receitas.html') 

@app.route('/receitas_omelete')
def receitas_omelete():
    return render_template('receitas_omelete.html')

# Contatos
@app.route('/contatos')
def contato():
    return render_template('contatos.html')   

# Restrições
@app.route('/restricao', methods=['GET', 'POST'])
def restricao():   
    if request.method == 'POST':
        dado = request.form.get('dado')
        flash("Restrição enviada com sucesso!")
        return redirect(url_for('restricao'))

    return render_template('restricao.html')

# Excluir conta
@app.route("/excluir_conta", methods=["POST"])
@login_required
def excluir_conta():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash("Conta excluída com sucesso.")
    return redirect(url_for("login"))

@app.route("/create")
def create():
    u = Usuario("Maria", "maria@gmail.com", "123456")
    db.session.add(u) 
    db.session.commit() 
    return 'Dados inseridos com sucesso'

@app.route("/select")
def select(): 
    u = Usuario.query.all() 
    if print(u) == Usuario.query.get(1):
     return u.nome

#update
@app.route("/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():
    if request.method == "POST":
        # Pegamos os novos dados do formulário
        current_user.nome = request.form["nome"]
        current_user.email = request.form["email"]
        
        # Se o usuário digitou um novo email  atualizamos
        novo_email = request.form.get("email")
        if  novo_email:
            current_user.email =  novo_email

        db.session.commit() # Salva as alterações no banco
        flash("Perfil atualizado com sucesso!")
        return redirect(url_for("perfilusuario"))

    return render_template("editar_perfil.html")

@app.route("/delete")
def delete():
     u = Usuario.query.get(1)
     db.session.delete(u) 
     db.session.commit() 
     return 'Dados excluídos com sucesso'

@app.errorhandler(401) 
def acesso_negado(e): 
    return render_template('acesso_negado.html'), 401


# Voltar página
@app.route("/voltar")
def voltar():
    return redirect(request.referrer or url_for("index"))


# ============================
# Rodando o app
# ============================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
