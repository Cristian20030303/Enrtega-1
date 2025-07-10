# Ingreso
# Importamos librerias y archivos
import csv
import datetime
import pandas as pd
from pathlib import Path
from datetime import datetime

# Importar funciones de utils/
from utils.helpers import obtener_id_usuario, limpiar_pantalla, obtener_tiempo_actual, contar_vehiculos_activos, hay_espacio_disponible  
from utils.validaciones import validar_cedula, validar_placa

# Rutas a los archivos CSV
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent 
DATA_DIR = project_root / "data" 

RUTA_PARQUEO = DATA_DIR / "parqueo.csv"
RUTA_USUARIOS = DATA_DIR / "usuarios.csv" 

def ingresar_vehiculo(id_usuario_existente: int = None, cedula_existente: str = None, 
                       placa_existente: str = None, tipo_vehiculo_existente: str = None):
    limpiar_pantalla() 
    print("\n--- INGRESO DE VEHÍCULO ---")
    
    if not hay_espacio_disponible(RUTA_PARQUEO): # Llama a la nueva función de helpers
        print("\n¡ATENCIÓN! El parqueadero ha alcanzado su capacidad máxima.")
        # helpers.MAX_CAPACIDAD_PARQUEADERO ya está disponible porque lo importamos implícitamente
        # y es una constante global en helpers.py.
        # Si prefieres ser explícito, podrías usar `from utils.helpers import MAX_CAPACIDAD_PARQUEADERO`
        # pero es más común acceder a constantes de módulos importados como `helpers.MAX_CAPACIDAD_PARQUEADERO`
        print(f"No se puede registrar el ingreso de más vehículos en este momento.")
        input("Presione Enter para continuar...")
        return # Sale de la función si no hay espacio
    # Asignar los valores de los argumentos opcionales o None
    id_usuario = id_usuario_existente
    cedula = cedula_existente
    placa = placa_existente
    tipo_vehiculo = tipo_vehiculo_existente

    # Pedimos la cédula para el ingreso del usuario, al no pedirse id
    if id_usuario is None:
        while True:
            cedula = input("Ingrese la cédula del usuario: ").strip() 
            if not validar_cedula(cedula):
                print("Cédula inválida. Por favor, ingrese una cédula numérica y con longitud válida.")
                input("Presione Enter para continuar...") 
                limpiar_pantalla()
                print("\n--- INGRESO DE VEHÍCULO ---") # Volvemos a imprimir el encabezado
            else:
                # 1. Obtener ID de usuario (y verificar si está registrado)
                id_usuario = obtener_id_usuario(cedula, RUTA_USUARIOS)
                if id_usuario is None:
                    print("El usuario no está registrado o hubo un problema al buscarlo. Por favor, registre al usuario primero.")
                    input("Presione Enter para continuar...")
                    return # Salir de la función
                else:
                    print(f"Usuario (ID: {id_usuario}) encontrado.") 
                    break # Salir del bucle de cédula
    else:
        print(f"Usando ID de usuario: {id_usuario} (proporcionado desde el registro).")

    # Pedimos la placa
    if RUTA_PARQUEO.exists() and RUTA_PARQUEO.stat().st_size > 0:
        try:
            df_parqueo = pd.read_csv(RUTA_PARQUEO)
            # Verificar si existe alguna fila para este id_usuario con hora_salida nula
            if not df_parqueo[(df_parqueo['id_usuario'] == id_usuario) & (df_parqueo['hora_salida'].isnull())].empty:
                print(f"ERROR: El usuario con ID '{id_usuario}' ya tiene un vehículo registrado en el parqueadero.")
                print("No se permite el ingreso de múltiples vehículos por la misma persona simultáneamente.")
                input("Presione Enter para continuar...")
                return
        except pd.errors.EmptyDataError:
            # Si el archivo existe pero está vacío, no hay vehículos activos, así que no hay conflicto.
            pass
        except Exception as e:
            print(f"ERROR: Ocurrió un problema al verificar vehículos activos del usuario: {e}")
            input("Presione Enter para continuar...")
            return
    if placa is None:
        while True:
            placa = input("Ingrese la placa del vehículo: ").strip().upper() 
            if not validar_placa(placa): 
                print("Formato de placa inválido. Debe ser como 'ABC123'.")
                input("Presione Enter para continuar...") 
                limpiar_pantalla()
                print("\n--- INGRESO DE VEHÍCULO ---") # Volver a imprimir el encabezado
            else:
                break
    
    # Pedimos el tipo de vehiculo aunque solo se admitan tipo carros pero es necesario especificar
    if tipo_vehiculo is None:
        tipo_vehiculo = input("Ingrese el tipo de vehículo (solo 'carro' permitido): ").lower().strip()
        if tipo_vehiculo != "carro": 
            print("ERROR: Este parqueadero es exclusivo para 'carros'.")
            input("Presione Enter para continuar...") 
            return
    elif tipo_vehiculo != "carro": # Si el tipo de vehiculo es distinto a 'carro'
        print(f"ADVERTENCIA: Tipo de vehículo '{tipo_vehiculo}' no permitido. Este parqueadero es exclusivo para 'carros'.")
        input("Presione Enter para continuar...") 
        return

    # Verificamos si no hay otro vehiculo estacionado por parte del mismo usuario
    if RUTA_PARQUEO.exists() and RUTA_PARQUEO.stat().st_size > 0:
        df_parqueo = pd.read_csv(RUTA_PARQUEO)
        
        # Filtramos para encontrar la placa Y que la hora_salida esté vacía (es decir, está activo)
        if not df_parqueo[(df_parqueo['placa'] == placa) & (df_parqueo['hora_salida'].isnull())].empty:
            print(f"El vehículo con placa '{placa}' ya se encuentra estacionado.")
            input("Presione Enter para continuar...")
            return

    

    
    # Creamos el registro del nuevo ingreso
    hora_ingreso = obtener_tiempo_actual() 

    nuevo_ingreso = {
        'placa': placa,
        'tipo_vehiculo': tipo_vehiculo,
        'id_usuario': id_usuario,
        'hora_ingreso': hora_ingreso,
        'hora_salida': '', # Vacío al inicio
        'valor_pagado': 0.0 # Cero al inicio
    }

    # Guardar en parqueo.csv (vehículos activos)
    try:
        file_exists = RUTA_PARQUEO.exists() and RUTA_PARQUEO.stat().st_size > 0
        
        with open(RUTA_PARQUEO, mode='a', newline='', encoding='utf-8') as file:
            # Utilizamos DictWriter para mantener el orden y nombres de columnas consistentes
            fieldnames = ['placa', 'tipo_vehiculo', 'id_usuario', 'hora_ingreso', 'hora_salida', 'valor_pagado']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader() # Escribir encabezado si el archivo es nuevo/vacío

            writer.writerow(nuevo_ingreso)
        print(f"Vehículo '{placa}' ingresado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el ingreso del vehículo: {e}")
    
    input("Presione Enter para continuar...")
