# Retiro del vehiculo

import csv
import datetime
from pathlib import Path
import pandas as pd

# Importamos funciones de otros módulos
from utils.tarifas import calcular_tarifa
from utils.helpers import limpiar_pantalla, obtener_tiempo_actual, \
    calcular_diferencia_minutos, calcular_costo_total
from utils.validaciones import validar_placa # Para validar el formato de la placa

# Rutas a los archivos csv
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
RUTA_PARQUEO = project_root / "data" / "parqueo.csv"
RUTA_HISTORIAL = project_root / "data" / "historial.csv"


# Tarifa por minuto
TARIFA_POR_MINUTO = 80.0

def retirar_vehiculo():
    limpiar_pantalla()
    print("\n--- RETIRO DE VEHÍCULO ---")
    
    placa_a_retirar = input("Ingrese la placa del vehículo a retirar: ").strip().upper()

    if not RUTA_PARQUEO.exists() or RUTA_PARQUEO.stat().st_size == 0:
        print("No hay vehículos registrados en el parqueadero (parqueo.csv está vacío o no existe).")
        input("Presione Enter para continuar...")
        return

    try:
        df_parqueo = pd.read_csv(RUTA_PARQUEO)
        
        # Filtramos con la placa del vehiculo y retiramos si esta activa
        vehiculo_para_retirar_df = df_parqueo[
            (df_parqueo['placa'] == placa_a_retirar) & 
            (df_parqueo['hora_salida'].isnull()) # Esta asegura que no se ha retirado
        ]

        if vehiculo_para_retirar_df.empty:
            print(f"El vehículo con placa '{placa_a_retirar}' no se encuentra actualmente en el parqueadero o ya ha sido retirado.")
            input("Presione Enter para continuar...")
            return
        
        
        vehiculo_info = vehiculo_para_retirar_df.iloc[0] 
        
        # Extraemos los datos necesarios para el historial y los cálculos
        hora_ingreso_str = vehiculo_info['hora_ingreso']
        hora_salida_str = obtener_tiempo_actual() # Obtenemos la hora actual del sistema

        print(f"DEBUG: Hora de ingreso (string desde CSV): '{hora_ingreso_str}'")
        print(f"DEBUG: Hora de salida (string actual): '{hora_salida_str}'")

        # Calcular tiempo de estadía
        tiempo_estadia_minutos = calcular_diferencia_minutos(hora_ingreso_str, hora_salida_str)

        if tiempo_estadia_minutos is None:
            print("ERROR: No se pudo calcular el tiempo de estadía. Verifique el formato de la hora o los datos en parqueo.csv.")
            input("Presione Enter para continuar...")
            return

        # Calculamos costo total
        costo_total = calcular_costo_total(tiempo_estadia_minutos, TARIFA_POR_MINUTO)

        
        # Preparamos el registro completo para historial.csv
        registro_historial = {
            'placa': vehiculo_info['placa'],
            'tipo_vehiculo': vehiculo_info['tipo_vehiculo'],
            'id_usuario': vehiculo_info['id_usuario'],
            'hora_ingreso': hora_ingreso_str,
            'hora_salida': hora_salida_str,
            'valor_pagado': costo_total 
        }

        # Guardamos el registro en historial.csv
        file_exists_historial = RUTA_HISTORIAL.exists() and RUTA_HISTORIAL.stat().st_size > 0
        
        with open(RUTA_HISTORIAL, mode='a', newline='', encoding='utf-8') as file:
            fieldnames_historial = ['placa', 'tipo_vehiculo', 'id_usuario', 'hora_ingreso', 'hora_salida', 'valor_pagado']
            writer_historial = csv.DictWriter(file, fieldnames=fieldnames_historial)

            if not file_exists_historial:
                writer_historial.writeheader() # Escribir encabezado si el archivo es nuevo/vacío

            writer_historial.writerow(registro_historial)
        print(f"Registro de retiro añadido a {RUTA_HISTORIAL.name}.")

        
        # Creamos un nuevo DataFrame que excluya la fila del vehículo retirado
        df_parqueo_actualizado = df_parqueo.drop(vehiculo_info.name) 

        # Guardamos el DF actualizado en parqueo.csv
        df_parqueo_actualizado.to_csv(RUTA_PARQUEO, index=False, quoting=csv.QUOTE_NONNUMERIC) 

        print(f"Vehículo '{placa_a_retirar}' retirado exitosamente del parqueadero activo.")
        print(f"Tiempo de estadía: {tiempo_estadia_minutos} minutos.")
        print(f"Costo total: ${costo_total:,.2f}")

    except FileNotFoundError:
        print(f"Error: El archivo de parqueo '{RUTA_PARQUEO.name}' no se encontró.")
    except pd.errors.EmptyDataError:
        print("El archivo de parqueo está vacío o corrupto.")
    except KeyError as e:
        print(f"Error: Columna faltante en parqueo.csv o historial.csv: {e}. Asegúrese de que todas las columnas necesarias existen.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al retirar el vehículo: {e}")
    
    input("Presione Enter para continuar...")
