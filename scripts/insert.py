#Importa a aplicação Flask
from app import app
#Importa o banco de dados
from utils import db
#Importa os models
from models import Usuario, Cardapio
#Permite usar o banco fora das rotas
with app.app_context():

    #Inserção de um novo usuário
    novo_usuario = Usuario(
        nome="Adina Warren",
        email="adina@email.com",
        senha="099"
    )

    #Inserção de um novo cardápio
    novo_cardapio = Cardapio(
        dia_semana="Segunda-feira",
        refeicao="Arroz, feijão, frango grelhado, salada e opção vegetariana"
    )

    #Adiciona os registros ao banco
    db.session.add(novo_usuario)
    db.session.add(novo_cardapio)

    #Confirma a inserção
    db.session.commit()

print("Dados inseridos com sucesso!")