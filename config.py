import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta')
    OPENAI_API_KEY = str(os.getenv('OPENAI_API_KEY'))
    