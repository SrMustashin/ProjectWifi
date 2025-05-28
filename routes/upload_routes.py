import os
from flask import Blueprint, request, render_template, redirect, flash, current_app
from core.excel import procesar_excel
from core.payments import enviar_pago

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/')
def index():
    return render_template('index.html', preview=None, resultados=None)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se envió ningún archivo')
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        flash('Nombre de archivo vacío')
        return redirect('/')

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = procesar_excel(filepath)
        resultados = [enviar_pago(row) for _, row in df.iterrows()]
        return render_template('index.html',
                               preview=df.to_dict(orient='records'),
                               resultados=resultados)
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}")
        return redirect('/')