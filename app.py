from flask import Flask
from routes.upload_routes import upload_bp
from pymongo import MongoClient
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Conectar a MongoDB Atlas
try:
    client = MongoClient(Config.MONGO_URI)
    client.admin.command('ping')  # Verifica conexión
    print("✅ Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar a MongoDB:", e)
    client = None

# Seleccionar base de datos si la conexión fue exitosa
if client:
    db = client.get_default_database()

# Crear carpeta para uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registrar rutas
app.register_blueprint(upload_bp)

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
