#Importa a aplicação Flask
from app import app
#Importa o banco de dados
from utils import db
#Importa os models
from models import Usuario, Cardapio
#Permite usar o banco fora das rotas
with app.app_context():
     #Remove um usuário pelo email
    usuario = Usuario.query.filter_by(email="lucas@email.com").first()

    if usuario:
        db.session.delete(usuario)

    #Remove o cardápio de sexta-feira
    cardapio = Cardapio.query.filter_by(dia_semana="Sexta-feira").first()

    if cardapio:
        db.session.delete(cardapio)

    #Confirma a remoção
    db.session.commit()

print("Dados removidos com sucesso!")