import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    print("=" * 60)
    print("Laboratorio IV - Ejercicio 2: Analisis de telemetria de nodo IOT")
    print("=" * 60)

    #cargar datos desde el archivo CSV
    file_path = "telemetria_nodo_iot.csv"
    df = pd.read_csv(
        file_path, parse_dates=['timestamp'], index_col='timestamp')

    print("\n[1]Datos cargados correctamente desde el archivo CSV.")
    print(f'     Total de registros: {len(df)}')
    print(
        '     Rango de fechas: desde'
        f' {df.index.min()} hasta {df.index.max()}'
    )

    #calcular estadisticas descriptivas
    columnas_numericas = [
        'temperatura_C',
        'humedad_pct',
        'voltaje_bateria_V',
        'rssi_dBm',
    ]
    estadisticas= pd.DataFrame({
        'Media': df[columnas_numericas].mean(),
        'Minimo': df[columnas_numericas].min(),
        'Maximo': df[columnas_numericas].max(),
        'Desviacion Estandar': df[columnas_numericas].std(),
    })

    print("\n[2]Estadisticas descriptivas de las variables numericas:")
    print(estadisticas.round(2))

    #arreglos numpy para voltaje y RSSI
    voltaje_arr = df['voltaje_bateria_V'].to_numpy()
    rssi_arr = df['rssi_dBm'].to_numpy()

    alerta_bateria = voltaje_arr < 3.5
    alerta_rssi = rssi_arr < -85
    alerta_general = alerta_bateria | alerta_rssi

    conteo_bateria = np.sum(alerta_bateria)
    conteo_rssi = np.sum(alerta_rssi)
    conteo_total = np.sum(alerta_general)

    print("\n[3] Conteo de Alertas :")
    print(f"     Bateria baja (voltaje<3.5V): {conteo_bateria} registros")
    print(f"     RSSI débil (rssi<-85dBm): {conteo_rssi} registros")
    print(f"     Al menos una alerta: {conteo_total} registros")

    #agregar columna de alerta al DataFrame
    df['alerta'] = alerta_general
    