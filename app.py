from flask import Flask
from routes.upload_routes import upload_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Crear carpeta de uploads si no existe
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(debug=True)
