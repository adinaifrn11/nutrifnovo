#Importa a aplicação Flask principal
#Necessário para usar o contexto da aplicação fora das rotas
from app import app
#Importa o objeto de conexão com o banco de dados (SQLAlchemy)
from utils import db
#Importa os models que representam as tabelas do banco
from models import Usuario, Cardapio
#permite acessar o banco fora das rotas
with app.app_context():
    #Criação de usuários fictícios
    #Dados de exemplo para simular um cenário real
    u1 = Usuario("Ana Clara Medeiros", "anaclara@email.com", "123")
    u2 = Usuario("João Barros", "joao@email.com", "456")
    u3 = Usuario("Tiago Barreto", "tiago@email.com", "768")
    u4 = Usuario("Mateus Santos", "mateus@email.com", "345")
    u5 = Usuario("Gabriel Moura", "gabriel@email.com", "107")
    u6 = Usuario("Isabelle Dantas", "isabelle@email.com", "223")
    u7 = Usuario("Daphne Ferreira", "daphne@email.com", "409")
    u8 = Usuario("Layla Silva", "layla@email.com", "380")
    u9 = Usuario("Adina Warren", "adina@email.com", "099")
    u10 = Usuario("Angela Winchester", "angela@email.com", "666")
    u11 = Usuario("Clara Potter", "clara@email.com", "011")

    #Criação de um cardápio fictício 
    #Contém o dia da semana e a refeição servida
    c1 = Cardapio(
        dia_semana="Segunda-Feira",
        refeicao="Arroz, feijão, frango grelhado, salada e opção vegetariana"
    )
    c2 = Cardapio(
        dia_semana="Terça-Feira",
        refeicao="Macarrão, feijão, figado, salada e opção vegetariana"
    )
    c3 = Cardapio(
        dia_semana="Quarta-Feira",
        refeicao="Arroz com passas, lentilha, feijão, frango e opção vegetariana"
    )
    c4 = Cardapio(
        dia_semana="Quinta-Feira",
        refeicao="Arroz, feijão, batata doce, peixe e opção vegetariana"
    )
    c5 = Cardapio(
        dia_semana="Sexta-Feira",
        refeicao="Arroz, feijão, batata gratinada, frango grelhado e opção vegetariana"
    )

    #Adiciona todos os objetos à sessão do banco
    db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, c1, c2, c3, c4, c5])
    #Confirma as alterações e grava os dados no banco
    db.session.commit()