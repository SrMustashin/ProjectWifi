from flask import Flask, redirect, url_for
from routes.upload_routes import upload_bp
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Crear carpeta para uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registrar rutas
app.register_blueprint(upload_bp)

# Ruta principal para redirigir a /upload
@app.route("/")
def index():
    return redirect(url_for("upload.upload_file"))

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
