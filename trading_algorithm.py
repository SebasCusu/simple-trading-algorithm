import yfinance as yf
import numpy as np
import sqlite3
import datetime

conn = sqlite3.connect('finance_data.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS history (ticker TEXT, fecha TEXT, precio actual REAL, senal TEXT)')

def descargar_datos(ticker):
    datos = yf.download(ticker, period="6mo", progress=False, group_by="ticker")

    if datos.empty:
        print("No hay datos disponibles")
        return None
    
    precios_ultimos_100 = datos[ticker]["Close"][-100:]
    precio_actual = float(precios_ultimos_100.iloc[-1])
    arreglo_precios = precios_ultimos_100.to_numpy()
    media_rapida = np.mean(arreglo_precios[-10:])
    media_lenta = np.mean(arreglo_precios[-50:])
    return precio_actual, media_rapida, media_lenta

ticker = "TSLA"
precio_actual, media_rapida, media_lenta = descargar_datos(ticker)


if media_rapida > media_lenta:
    senal = "Compra"

if media_lenta < media_rapida:
    senal = "Venta"

else:
    senal = "Neutral"

fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")


cur.execute('INSERT INTO history VALUES (?, ?, ?, ?)',(ticker, fecha_hoy, precio_actual, senal))
conn.commit()

cur.execute('SELECT * FROM history')
datos_guardados = cur.fetchall()
print(datos_guardados)