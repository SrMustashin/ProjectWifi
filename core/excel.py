import pandas as pd

def generar_transaccion_reproducible(idcliente, telefono, monto, fecha_pago):
    """
    Genera un ID único reproducible en base a:
    idcliente + últimos 3 dígitos de telefono + monto + fecha (DDMMYYYY) + hora (HHMM)
    """
    ult3_telefono = str(telefono)[-3:] if pd.notna(telefono) else "000"

    # Manejar monto faltante
    if pd.isna(monto):
        monto_str = "0"
    else:
        monto_str = str(int(float(monto)))  # solo parte entera del monto
        # monto_str = str(monto)  # si quieres conservar decimales

    # Manejar fecha faltante
    if pd.isna(fecha_pago):
        fecha_part = "01011970"
        hora_part = "0000"
    else:
        fecha_dt = pd.to_datetime(fecha_pago)
        fecha_part = fecha_dt.strftime("%d%m%Y")  # DDMMYYYY
        hora_part = fecha_dt.strftime("%H%M")      # HHMM

    return f"{idcliente}{ult3_telefono}{monto_str}{fecha_part}{hora_part}"

def procesar_excel(filepath):
    try:
        # Leer las columnas necesarias
        df = pd.read_excel(filepath, engine="openpyxl", usecols=[
            "Descripción", "Importe de crédito", "Fecha del apunte",
            "Hora de cargo o abono", "Referencia de cliente"
        ])

        # Renombrar columnas
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df.rename(columns={
            "Descripción": "descripcion",
            "Importe de crédito": "monto",
            "Fecha del apunte": "fecha_pago",
            "Hora de cargo o abono": "hora_pago",
            "Referencia de cliente": "referencia_cliente"
        }, inplace=True)

        # Separar idcliente y telefono
        split_cols = df['descripcion'].astype(str).str.strip().str.split(' ', n=1, expand=True)
        df['idcliente'] = split_cols[0]
        df['telefono'] = split_cols[1]

        # Convertir fecha
        df['fecha_pago'] = pd.to_datetime(df['fecha_pago'], dayfirst=True, errors='coerce')

        # Guardar columna original de hora como texto
        hora_str = df['hora_pago'].astype(str).str.strip()

        # Intentar parseo con HH:MM
        horas = pd.to_datetime(hora_str, format='%H:%M', errors='coerce')

        # Donde falle, intentar con HH:MM:SS
        mask_na = horas.isna()
        if mask_na.any():
            horas2 = pd.to_datetime(hora_str[mask_na], format='%H:%M:%S', errors='coerce')
            horas.update(horas2)

        # Extraer solo la hora
        df['hora_pago'] = horas.dt.time

        # Eliminar filas sin fecha u hora
        df = df.dropna(subset=['fecha_pago', 'hora_pago', 'idcliente', 'telefono', 'monto'])

        # Unir fecha y hora
        df['fecha_pago'] = df.apply(
            lambda row: f"{row['fecha_pago'].strftime('%Y-%m-%d')} {row['hora_pago']}", axis=1
        )

        # Generar transaccion reproducible
        df['transaccion'] = df.apply(
            lambda row: generar_transaccion_reproducible(
                row['idcliente'], row['telefono'], row['monto'], row['fecha_pago']
            ),
            axis=1
        )

        return df[['idcliente', 'telefono', 'transaccion', 'monto', 'fecha_pago']]

    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        return pd.DataFrame(columns=['idcliente', 'telefono', 'transaccion', 'monto', 'fecha_pago'])
