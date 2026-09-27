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

    #Generar grafico de evolucion temporal de telemetria y eventos de alerta
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    color_temp = '#d95f02'
    color_volt = '#1b9e77'

    ax_top.plot(
        df.index, 
        df['temperatura_C'], 
        color=color_temp, 
        label='Temperatura (°C)',
        linewidth=1.2,
        )
    ax_top.set_ylabel(
        'Temperatura (°C)', color=color_temp, fontsize=10, fontweight='bold')

    ax_top.tick_params(axis='y', labelcolor=color_temp)
    ax_top.grid(True, linestyle='--', alpha=0.6)

    ax_volt = ax_top.twinx()
    ax_volt.plot(
        df.index, 
        df['voltaje_bateria_V'], 
        color=color_volt, 
        label='Voltaje Bateria (V)',
        linewidth=1.2,
        )
    ax_volt.set_ylabel(
        'Voltaje Bateria (V)', color=color_volt, fontsize=10, fontweight='bold')

    ax_volt.tick_params(axis='y', labelcolor=color_volt)

    #destacar puntos de alerta
    tiempos_alerta = df.index[alerta_general]
    volt_alerta = df.loc[alerta_general, 'voltaje_bateria_V']
    ax_volt.scatter(
        tiempos_alerta,
        volt_alerta,
        color='red',
        zorder=5,
        s=30,
        label='Alerta Detectada'
    )

    ax_top.set_title(
        'Evolución Temporal de Telemetría y Alertas',
        fontsize=12,
        fontweight='bold'
    )

    #panel inferior: RSSI
    color_rssi = '#7570b3'
    ax_bot.plot(
        df.index,
        df['rssi_dBm'],
        color=color_rssi,
        label=' Señal RSSI (dBm)',
        linewidth=1,
    )

    ax_bot.axhline(
        -85, color='red', linestyle=':', linewidth=1.5, label='Umbral RSSI (-85 dBm)')

    ax_bot.set_ylabel(
        'RSSI (dBm)', color=color_rssi, fontsize=10, fontweight='bold')

    ax_bot.set_xlabel('Fecha y Hora', fontsize=10, fontweight='bold')
    ax_bot.grid(True, linestyle='--', alpha=0.6)

    rssi_alerta_times = df.index[alerta_rssi]
    rssi_alerta_vals = df.loc[alerta_rssi, 'rssi_dBm']
    ax_bot.scatter(
        rssi_alerta_times,
        rssi_alerta_vals,
        color='red',
        zorder=5,
        s=35,
        marker='x',
        label='Alerta RSSI'
    )
    ax_bot.legend(loc='lower right')

    plt.tight_layout()
    plt.savefig('grafico_telemetria_iot.png', dpi=300)
    