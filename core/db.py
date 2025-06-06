from pymongo import MongoClient
from config import Config

def get_mongo_db():
    client = MongoClient(Config.MONGO_URI)
    # Conectar a la base de datos específica
    db = client["MainDB"]  # Cambia por el nombre real si es diferente
    return db

