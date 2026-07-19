from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Entrar")

class CadastroForm(FlaskForm):

    nome = StringField(
        "Nome",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    submit = SubmitField("Cadastrar")    

class CardapioForm(FlaskForm):

    dia_semana = StringField(
        "Dia da Semana",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    refeicao = TextAreaField(
        "Refeição",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    submit = SubmitField("Salvar Cardápio")    