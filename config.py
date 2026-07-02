import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUAP_CLIENT_ID = os.getenv("SUAP_CLIENT_ID")
    SUAP_CLIENT_SECRET = os.getenv("SUAP_CLIENT_SECRET")