#Importa a aplicação Flask
from app import app
#Importa o banco de dados
from utils import db
#Importa os models
from models import Usuario, Cardapio
#Permite usar o banco fora das rotas
with app.app_context():
    #Atualiza o nome de um usuário
    usuario = Usuario.query.filter_by(email="adina@email.com").first()

    if usuario:
        usuario.nome = "Adina Lourrane Santos"

    #Atualiza a refeição de um dia específico
    cardapio = Cardapio.query.filter_by(dia_semana="Segunda-feira").first()

    if cardapio:
        cardapio.refeicao = "Arroz integral, feijão, frango grelhado, legumes e opção vegetariana"

    #Confirma a atualização
    db.session.commit()

print("Dados atualizados com sucesso!")