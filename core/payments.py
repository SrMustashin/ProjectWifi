import requests
from config import Config
from datetime import datetime

# Mapeo de códigos de error de iWisp a mensajes legibles
ERRORS_IWISP = {
    200: "Pago registrado correctamente",
    400: "La conexión con la API no se pudo completar.",
    403: "El monto no es un número, o no es mayor a 0.00",
    404: "No hay fecha de creación, la fecha está vacía o no es una fecha válida",
    405: "La transacción ya existe",
    406: "El número de celular no es de 10 dígitos",
    407: "El ID CLIENTE o el número de celular no corresponde a un cliente",
    408: "El plan prepago no existe o no es válido para el cliente seleccionado",
    409: "La petición contiene un paquete de mensualidades pero no contiene una conexión",
    410: "El paquete de mensualidades no existe o no es válido para el cliente seleccionado",
    411: "El motivo de la cobranza es inválido.",
    412: "El tipo de transacción es inválido.",
    413: "El anticipo es inválido.",
    500: "Error interno del servidor iWisp"
}

def enviar_pago(row):
    # Formatear fecha
    if isinstance(row["fecha_pago"], datetime):
        fecha_pago = row["fecha_pago"].strftime("%Y-%m-%d %H:%M:%S")
    else:
        fecha_pago = str(row["fecha_pago"]).split(".")[0]

    payload = {
        "api_key": Config.IWISP_API_KEY,
        "idcliente": int(row["idcliente"]),
        "telefono": str(row["telefono"]),
        "transaccion": str(row["transaccion"]),
        "monto": f"{float(row['monto']):.2f}",
        "fecha_pago": fecha_pago
    }

    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(Config.IWISP_API_URL, json=payload, headers=headers)

        # Intentar parsear JSON
        try:
            data = r.json()
            status_real = data.get("status", r.status_code)
            mensaje_real = data.get("message") or data.get("mensaje") or ERRORS_IWISP.get(r.status_code, "Error desconocido")
        except ValueError:
            # Si no es JSON, usar el texto o el mapa de errores
            status_real = r.status_code
            mensaje_real = r.text if r.text else ERRORS_IWISP.get(r.status_code, "Error desconocido")

        return {
            "idcliente": row["idcliente"],
            "status": status_real,
            "mensaje": mensaje_real
        }

    except Exception as ex:
        return {
            "idcliente": row["idcliente"],
            "status": "Error",
            "mensaje": str(ex)
        }
