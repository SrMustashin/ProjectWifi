import requests
import json
from config import Config
from datetime import datetime

def enviar_pago(row):
    # Asegurar formato de fecha
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
        print("Enviando a la API:")
        print("Headers:", headers)
        print("JSON que se envía:", json.dumps(payload, ensure_ascii=False))

        r = requests.post(Config.IWISP_API_URL, json=payload, headers=headers)

        print("Respuesta cruda:", r.text)

        contenido = r.json() if r.headers.get("Content-Type", "").startswith("application/json") else r.text

        return {
            "idcliente": row["idcliente"],
            "status": r.status_code,
            "mensaje": contenido
        }
    except Exception as ex:
        return {
            "idcliente": row["idcliente"],
            "status": "Error",
            "mensaje": str(ex)
        }
