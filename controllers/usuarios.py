from utils import lm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import Usuario
from utils import db

bp_usuarios = Blueprint('usuarios', __name__)

#Criando função user_loader
@lm.user_loader
def load_user(id):
    usuario = Usuario.query.get(int(id))
    return usuario

#Criando a rota autenticar
from flask_login import login_user

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:
        login_user(usuario)
        return redirect(url_for('usuarios.dashboard'))
    else:
        flash('Email ou senha incorretos')
        return redirect(url_for('usuarios.login'))

#Criando rota de logout
@bp_usuarios.route('/logoff')
def logoff():
    logout_user()
    return redirect(url_for('usuarios.login'))

#Protegendo rotas com login_required
@bp_usuarios.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

    

