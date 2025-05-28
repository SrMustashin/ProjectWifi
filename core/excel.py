import pandas as pd

def procesar_excel(filepath):
    df = pd.read_excel(filepath, engine="openpyxl", usecols=[
        "Descripción", "Importe de crédito", "Fecha del apunte",
        "Hora de cargo o abono", "Referencia de cliente"
    ])

    df.rename(columns={
        "Descripción": "descripcion",
        "Importe de crédito": "monto",
        "Fecha del apunte": "fecha_pago",
        "Hora de cargo o abono": "hora_pago",
        "Referencia de cliente": "transaccion"
    }, inplace=True)

    split_cols = df['descripcion'].astype(str).str.strip().str.split(' ', n=1, expand=True)
    if split_cols.shape[1] != 2:
        raise ValueError("Cada 'Descripción' debe tener dos valores: ID y teléfono.")
    df['idcliente'] = split_cols[0]
    df['telefono'] = split_cols[1]

    df['fecha_pago'] = pd.to_datetime(df['fecha_pago'], dayfirst=True, errors='coerce')
    df['hora_pago'] = pd.to_datetime(df['hora_pago'], format='%H:%M:%S', errors='coerce').dt.time

    df = df.dropna(subset=['fecha_pago', 'hora_pago'])
    df['fecha_pago'] = df.apply(lambda row: f"{row['fecha_pago'].date()} {row['hora_pago']}", axis=1)

    return df[['idcliente', 'telefono', 'transaccion', 'monto', 'fecha_pago']]
