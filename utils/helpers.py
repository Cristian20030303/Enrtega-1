import csv
from datetime import datetime, timedelta
from pathlib import Path
import os
import pandas as pd
import math

# --- Funciones Generales ---

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

def calcular_costo_total(tiempo_minutos: int) -> float: # Eliminamos 'tarifa_por_minuto' como parámetro
    """
    Calcula el costo total del parqueo basado en el tiempo en minutos y las reglas de cobro.

    Reglas de cobro:
    - $7.000 por hora completa.
    - $1.500 por cada cuarto de hora adicional.
    - El pago mínimo es de $7.000.
    """
    # Definición de tarifas fijas según tus requisitos
    VALOR_HORA_COMPLETA = 7000.0
    VALOR_CUARTO_HORA = 1500.0
    
    # Manejo de casos de tiempo negativo o cero
    if tiempo_minutos <= 0:
        return VALOR_HORA_COMPLETA # Siempre se cobra el mínimo si no hubo tiempo o es negativo

    # Convertir tiempo en minutos a horas y minutos para el cálculo
    horas_totales_flotante = tiempo_minutos / 60.0
    
    # Calcular horas enteras parqueadas (ej. 1.5 horas -> 1 hora entera)
    horas_enteras = math.floor(horas_totales_flotante)
    
    # Calcular minutos restantes después de las horas enteras (ej. 1.5 horas -> 0.5 horas * 60 = 30 minutos)
    minutos_restantes = tiempo_minutos % 60
    
    # Calcular cuartos de hora a partir de los minutos restantes
    # math.ceil asegura que incluso 1 minuto adicional se redondea a 1 cuarto de hora
    cuartos_de_hora = math.ceil(minutos_restantes / 15)
    
    # Calcular el cobro basado en horas enteras
    cobro_por_horas = horas_enteras * VALOR_HORA_COMPLETA
    
    # Calcular el cobro basado en cuartos de hora
    cobro_por_cuartos = cuartos_de_hora * VALOR_CUARTO_HORA
    
    # Sumar ambos cobros
    costo_calculado = cobro_por_horas + cobro_por_cuartos
    
    # Aplicar la condición de pago mínimo
    if costo_calculado < VALOR_HORA_COMPLETA:
        return VALOR_HORA_COMPLETA # Si el cálculo es menor a $7.000, se cobra $7.000
    else:
        return costo_calculado
# --- Funciones de Acceso a Datos (usuarios.csv) ---

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

def generar_id_unico(users_file_path: Path) -> int | None:
    """
    Genera un ID único para un nuevo usuario, limitado a un máximo de 50 IDs.
    Busca el primer ID disponible entre 1 y 50.
    """
    MAX_USERS = 50
    existing_ids = set()

    if users_file_path.exists() and users_file_path.stat().st_size > 0:
        try:
            df_usuarios = pd.read_csv(users_file_path)
            if 'id' in df_usuarios.columns:
                existing_ids = set(df_usuarios['id'].dropna().astype(int).tolist())
            else:
                print(f"ADVERTENCIA (helpers.generar_id_unico): La columna 'id' no se encontró en '{users_file_path.name}'.")
        except pd.errors.EmptyDataError:
            pass
        except Exception as e:
            print(f"ERROR (helpers.generar_id_unico): No se pudo leer IDs existentes: {e}")
            return None

    if len(existing_ids) >= MAX_USERS:
        print(f"ERROR: Se ha alcanzado el límite máximo de {MAX_USERS} usuarios registrados. No se pueden registrar más.")
        return None

    for i in range(1, MAX_USERS + 1):
        if i not in existing_ids:
            return i

    print(f"ERROR: No se encontró un ID único disponible entre 1 y {MAX_USERS}.")
    return None
# --- Funciones de Acceso a Datos (parqueo.csv) ---

def contar_vehiculos_activos(parqueo_file_path: Path) -> int:
    """
    Cuenta el número de vehículos actualmente estacionados en el parqueadero.
    """
    activos = 0
    try:
        if not parqueo_file_path.exists() or parqueo_file_path.stat().st_size == 0:
            return 0 

        # Mejor usar pandas para esto si ya lo importas
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
