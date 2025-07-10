import csv
from datetime import datetime, timedelta
from pathlib import Path
import os
import pandas as pd
import math


MAX_CAPACIDAD_PARQUEADERO = 50

# Definimos las funciones generales para el programa
def obtener_tiempo_actual():
    """Devuelve la fecha y hora actual formateada como 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def limpiar_pantalla():
    """Limpia la consola."""
    # Para Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Para Mac y Linux
    else:
        _ = os.system('clear')

def calcular_diferencia_minutos(inicio: str, fin: str) -> int | None:
    """
    Calcula la diferencia en minutos entre dos timestamps en formato 'YYYY-MM-DD HH:MM:SS'.
    Retorna la diferencia en minutos como entero, o None si hay un error de formato.
    """
    try:
        inicio_dt = datetime.strptime(inicio.strip(), '%Y-%m-%d %H:%M:%S')
        fin_dt = datetime.strptime(fin.strip(), '%Y-%m-%d %H:%M:%S')
        diferencia = fin_dt - inicio_dt
        return int(diferencia.total_seconds() / 60)
    except ValueError as e:
        print(f"[ERROR] (calcular_diferencia_minutos) Formato de fecha/hora inválido. Inicio: '{inicio}', Fin: '{fin}'. Error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] (calcular_diferencia_minutos) Ocurrió un error inesperado: {e}")
        return None

def calcular_costo_total(tiempo_minutos: int) -> float:
    """
    Calcula el costo total del parqueo basado en el tiempo en minutos y las reglas de cobro.

    Reglas de cobro:
    - $7.000 por hora completa.
    - $1.500 por cada cuarto de hora adicional.
    - El pago mínimo es de $7.000.
    """
    # Definimos las tarifas fijas según los requisitos
    VALOR_HORA_COMPLETA = 7000.0
    VALOR_CUARTO_HORA = 1500.0
    
    # Manejo de casos de tiempo negativo o cero
    if tiempo_minutos <= 0:
        return VALOR_HORA_COMPLETA # Siempre se cobra el mínimo si no hubo tiempo o es negativo

    # Convertimos el tiempo en minutos a horas y minutos para el cálculo
    horas_totales_flotante = tiempo_minutos / 60.0
    
    # Calculamos horas enteras parqueadas
    horas_enteras = math.floor(horas_totales_flotante)
    
    # Calculamos minutos restantes después de las horas enteras
    minutos_restantes = tiempo_minutos % 60
    
    # Calculamos cuartos de hora a partir de los minutos restantes
    # math.ceil asegura que incluso 1 minuto adicional se redondea a 1 cuarto de hora
    cuartos_de_hora = math.ceil(minutos_restantes / 15)
    
    # Calculamos el cobro basado en horas enteras
    cobro_por_horas = horas_enteras * VALOR_HORA_COMPLETA
    
    # Calculamos el cobro basado en cuartos de hora
    cobro_por_cuartos = cuartos_de_hora * VALOR_CUARTO_HORA
    
    # Sumamos ambos cobros
    costo_calculado = cobro_por_horas + cobro_por_cuartos
    
    # Aplicamos la condición de pago mínimo
    if costo_calculado < VALOR_HORA_COMPLETA:
        return VALOR_HORA_COMPLETA # Si el cálculo es menor a $7.000, se cobra $7.000
    else:
        return costo_calculado

# Definimos las funciones de acceso a usuarios.csv
def usuario_registrado(cedula: str, users_file_path: Path) -> bool:
    """
    Verifica si un usuario con la cédula especificada ya está registrado en el archivo.
    """
    if not users_file_path.exists() or users_file_path.stat().st_size == 0:
        return False

    try:
        with open(users_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None or 'cedula' not in reader.fieldnames:
                # Si no hay encabezados o no está la columna 'cedula', asumir no registrado
                return False
            for row in reader:
                if row['cedula'] == cedula:
                    return True
        return False
    except Exception as e:
        print(f"Error al verificar usuario registrado: {e}")
        return False

def obtener_id_usuario(cedula: str, users_file_path: Path) -> int | None:
    """
    Obtiene el ID de usuario dado una cédula desde el archivo de usuarios especificado.
    """
    try:
        if not users_file_path.exists():
            print(f"DEBUG (helpers): Archivo de usuarios NO encontrado en: {users_file_path}")
            return None
        
        if users_file_path.stat().st_size == 0:
            print(f"DEBUG (helpers): Archivo de usuarios VACÍO en: {users_file_path}")
            return None
        
        print(f"DEBUG (helpers): Archivo de usuarios encontrado y no vacío: {users_file_path}")
            
        with open(users_file_path, mode="r", newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if headers is None: 
                print("DEBUG (helpers): Archivo de usuarios sin encabezados.")
                return None

            if 'cedula' not in headers or 'id' not in headers:
                print(f"[ERROR] (helpers.obtener_id_usuario) Columnas 'cedula' o 'id' no encontradas en los encabezados de '{users_file_path.name}'.")
                print(f"DEBUG (helpers): Encabezados encontrados: {headers}")
                return None
            
            cedula_col_index = headers.index('cedula')
            id_col_index = headers.index('id')

            for row_num, row in enumerate(reader):
                if row and len(row) > cedula_col_index and len(row) > id_col_index:
                    print(f"DEBUG (helpers): Leyendo fila {row_num + 2}: {row}")
                    if row[cedula_col_index] == cedula:
                        print(f"DEBUG (helpers): Cédula '{cedula}' encontrada en fila {row_num + 2}. ID: '{row[id_col_index]}'")
                        try:
                            return int(row[id_col_index]) 
                        except ValueError:
                            print(f"[ADVERTENCIA] (helpers.obtener_id_usuario) ID de usuario '{row[id_col_index]}' no es numérico para cédula '{cedula}'.")
                            return None 
            print(f"DEBUG (helpers): Cédula '{cedula}' NO encontrada después de buscar en todo el archivo.")
            return None 
    except Exception as e:
        print(f"[ERROR] (helpers.obtener_id_usuario) Ocurrió un error al obtener ID de usuario: {e}")
        return None

def generar_id_unico(users_file_path: Path) -> int:
    """
    ### MODIFICACIÓN: La lógica de esta función se cambió por completo.
    ### Ahora genera un ID único secuencial para un nuevo usuario, sin límite.
    ### El ID será el último ID existente + 1, o 1 si no hay usuarios.
    """
    if not users_file_path.exists() or users_file_path.stat().st_size == 0:
        return 1  # Primer ID si el archivo no existe o está vacío

    try:
        df_usuarios = pd.read_csv(users_file_path)
        if 'id' in df_usuarios.columns and not df_usuarios['id'].empty:
            # Encuentra el ID máximo y suma 1. Asegura que los IDs sean enteros.
            # Dropna por si hay valores NaN en la columna 'id'
            # astype(int) para asegurar que el tipo de datos sea entero antes de max()
            return int(df_usuarios['id'].dropna().astype(int).max()) + 1
        else:
            print(f"ADVERTENCIA (helpers.generar_id_unico): La columna 'id' no se encontró o está vacía en '{users_file_path.name}'. Generando ID 1.")
            return 1 # Si no hay columna ID o está vacía, empezar desde 1
    except pd.errors.EmptyDataError:
        return 1  # Si el CSV existe pero está vacío, empezar desde 1
    except Exception as e:
        print(f"ERROR (helpers.generar_id_unico): No se pudo leer IDs existentes para generar uno nuevo. Error: {e}. Generando ID 1.")
        return 1 

def contar_vehiculos_activos(parqueo_file_path: Path) -> int:
    """
    Cuenta el número de vehículos actualmente estacionados en el parqueadero.
    """
    activos = 0
    try:
        if not parqueo_file_path.exists() or parqueo_file_path.stat().st_size == 0:
            return 0 

       
        try:
            df = pd.read_csv(parqueo_file_path)
            if 'hora_salida' in df.columns:
                activos = df['hora_salida'].isnull().sum() 
            else:
                # Si no hay columna hora_salida, el conteo de activos es el total de entradas.
                activos = len(df)
        except pd.errors.EmptyDataError:
            return 0 # Archivo CSV existe pero está vacío
        except Exception as pd_e:
            print(f"Error con pandas al contar vehículos activos: {pd_e}. Intentando con csv.DictReader.")
            # Fallback a csv.DictReader si pandas falla inesperadamente
            with open(parqueo_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames and 'hora_salida' in reader.fieldnames:
                    for row in reader:
                        if 'hora_salida' not in row or not row['hora_salida']:
                            activos += 1
    except Exception as e:
        print(f"Error al contar vehículos activos: {e}")
    return activos
def hay_espacio_disponible(parqueo_file_path: Path) -> bool:
    """
    Verifica si hay espacio disponible en el parqueadero basado en la capacidad máxima definida.
    """
    vehiculos_activos = contar_vehiculos_activos(parqueo_file_path)
    # Encontramos el espacio disponible restandole a la maxima capacidad del parqueadero, la cantidad de vehiculos dentro
    espacio_disponible = MAX_CAPACIDAD_PARQUEADERO - vehiculos_activos
    
    if espacio_disponible > 0:
        print(f"DEBUG (helpers): Espacio disponible: {espacio_disponible} celdas. Total activos: {vehiculos_activos}/{MAX_CAPACIDAD_PARQUEADERO}.")
        return True
    else:
        print(f"DEBUG (helpers): No hay espacio disponible. Parqueadero lleno ({vehiculos_activos}/{MAX_CAPACIDAD_PARQUEADERO}).")
        return False
