from flask import Flask
from flask_cors import CORS
from routes import register_routes
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) 
app.config.from_object(Config)

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
    
