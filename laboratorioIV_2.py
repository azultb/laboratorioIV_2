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