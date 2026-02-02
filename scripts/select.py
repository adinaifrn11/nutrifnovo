#Importa a aplicação Flask
from app import app
#Importa o banco de dados
from utils import db
#Importa os models
from models import Usuario, Cardapio
#Permite usar o banco fora das rotas
with app.app_context():
    #Consulta todos os usuários
    usuarios = Usuario.query.all()

    print("Lista de usuários:")
    for u in usuarios:
        print(u.nome, "-", u.email)

    # Consulta todos os cardápios
    cardapios = Cardapio.query.all()

    print("\nCardápio da semana:")
    for c in cardapios:
        print(c.dia_semana, "->", c.refeicao)