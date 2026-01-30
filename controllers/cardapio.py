from utils import db

class Cardapio(db.Model):
    __tablename__ = "cardapio"

    id = db.Column(db.Integer, primary_key=True)
    nome_prato = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    def __init__(self, nome_prato, descricao):
        self.nome_prato = nome_prato
        self.descricao = descricao

    def __repr__(self):
        return f"<Cardapio {self.nome_prato}>"

