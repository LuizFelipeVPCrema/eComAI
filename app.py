from flask import Flask
from routes import register_routes
# from database.db import initialize_db
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)


# Inicializar banco de dados
# initialize_db(app)

# Registrar rotas
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
    
