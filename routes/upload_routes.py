from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.excel import procesar_excel
from core.payments import enviar_pago

upload_bp = Blueprint("upload", __name__)

# Página principal
@upload_bp.route("/")
def index():
    return render_template("index.html")

# Subida de Excel y vista previa
@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No se envió ningún archivo", "error")
            return redirect(url_for("upload.index"))

        file = request.files["file"]
        if file.filename == "":
            flash("El archivo no tiene nombre", "error")
            return redirect(url_for("upload.index"))

        try:
            registros = procesar_excel(file)

            if registros.empty:
                flash("No se encontraron registros válidos en el archivo", "error")
                return redirect(url_for("upload.index"))

            # Convertir a lista de diccionarios para Jinja
            registros_list = registros.to_dict(orient="records")

            return render_template("preview.html", registros=registros_list)

        except Exception as e:
            flash(f"Error al procesar el archivo: {e}", "error")
            return redirect(url_for("upload.index"))

    return render_template("index.html")

# Procesar pagos seleccionados
@upload_bp.route("/procesar", methods=["POST"])
def procesar():
    try:
        seleccionados = request.form.getlist("seleccionados")

        if not seleccionados:
            flash("No seleccionaste ningún registro", "error")
            return redirect(url_for("upload.index"))

        resultados = []
        exitosos = 0
        errores = 0

        for seleccionado in seleccionados:
            try:
                datos = seleccionado.split("|")
                if len(datos) != 5:
                    resultados.append({
                        "idcliente": "",
                        "status": "SKIPPED",
                        "mensaje": "Formato de registro incorrecto"
                    })
                    errores += 1
                    continue

                row = {
                    "idcliente": datos[0].strip(),
                    "telefono": datos[1].strip(),
                    "transaccion": datos[2].strip(),
                    "monto": datos[3].strip(),
                    "fecha_pago": datos[4].strip()
                }

                if not row["idcliente"] or float(row["monto"]) <= 0:
                    resultados.append({
                        "idcliente": row["idcliente"],
                        "status": "SKIPPED",
                        "mensaje": "Registro inválido: cliente o monto vacío"
                    })
                    errores += 1
                    continue

                resultado = enviar_pago(row)
                resultados.append(resultado)

                if resultado["status"] == 200:
                    exitosos += 1
                else:
                    errores += 1

            except Exception as e_fila:
                resultados.append({
                    "idcliente": "",
                    "status": "ERROR",
                    "mensaje": f"Error procesando fila: {str(e_fila)}"
                })
                errores += 1

        resumen = {"insertados": exitosos, "errores": errores}
        return render_template("index.html", resultados=resultados, resumen=resumen)

    except Exception as e:
        flash(f"Error general al procesar pagos: {e}", "error")
        return redirect(url_for("upload.index"))
