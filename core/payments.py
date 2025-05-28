import requests
from config import Config

def enviar_pago(row):
    payload = {
        "api_key": Config.IWISP_API_KEY,
        "idcliente": str(row["idcliente"]),
        "telefono": str(row["telefono"]),
        "transaccion": str(row["transaccion"]),
        "monto": float(row["monto"]),
        "fecha_pago": row["fecha_pago"]
    }

    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(Config.IWISP_API_URL, json=payload, headers=headers)
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
