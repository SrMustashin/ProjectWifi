import os
from flask import Blueprint, request, render_template, redirect, flash, current_app
from core.excel import procesar_excel
from core.payments import enviar_pago
from core.db import get_mongo_db

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
        # Procesar el Excel a DataFrame
        df = procesar_excel(filepath)

        # Obtener la colección de MongoDB
        db = get_mongo_db()
        payments_collection = db["PAYMENTS"]

        # Convertir DataFrame a lista de diccionarios
        documentos = df.to_dict(orient='records')
        documentos_nuevos = []
        transacciones_duplicadas = []

        for doc in documentos:
            transaccion = doc.get("transacción") or doc.get("Transacción")
            if transaccion and not payments_collection.find_one({"transacción": transaccion}):
                documentos_nuevos.append(doc)
            else:
                transacciones_duplicadas.append(transaccion)

        # Insertar los documentos nuevos
        if documentos_nuevos:
            payments_collection.insert_many(documentos_nuevos)

        # Crear resumen
        resumen = {
            "insertados": len(documentos_nuevos),
            "duplicados": len(transacciones_duplicadas)
        }

        # Enviar pagos y mostrar todo
        resultados = [enviar_pago(row) for _, row in df.iterrows()]
        return render_template('index.html',
                               preview=df.to_dict(orient='records'),
                               resultados=resultados,
                               resumen=resumen)

    except Exception as e:
        flash(f"Error al procesar el archivo: {e}")
        return redirect('/')