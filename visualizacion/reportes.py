



import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# --- Configuración de Rutas de Datos (Robustas) ---
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
DATA_DIR = project_root / "data"
# --- Fin Configuración de Rutas ---

def _load_csv_or_handle_error(file_path: Path, df_name: str) -> pd.DataFrame | None:
    """Función auxiliar para cargar CSVs con manejo de errores."""
    try:
        # Asegurarse de que el archivo no esté vacío (solo encabezados) antes de intentar leer
        # pd.read_csv con pd.errors.EmptyDataError ya maneja archivos con 0 bytes,
        # pero esto añade una capa extra para archivos con solo encabezados.
        if file_path.exists() and file_path.stat().st_size == 0:
            print(f"INFO: El archivo '{file_path.name}' está vacío. No hay datos para el {df_name}.")
            return None
        
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"INFO: El archivo '{file_path.name}' no se encontró. No hay datos para el {df_name}.")
        return None
    except pd.errors.EmptyDataError:
        print(f"INFO: El archivo '{file_path.name}' está vacío (posiblemente solo encabezados). No hay datos para el {df_name}.")
        return None
    except Exception as e:
        print(f"ERROR: No se pudo cargar el archivo '{file_path.name}' para el {df_name}. Detalle: {e}")
        return None

def reporte_vehiculos_activos():
    parqueo_path = DATA_DIR / "parqueo.csv"
    df = _load_csv_or_handle_error(parqueo_path, "reporte de vehículos activos")
    if df is None:
        return

    print("\n--- Vehículos actualmente en el parqueadero ---")
    if df.empty:
        print("No hay vehículos estacionados actualmente.")
    else:
        # Mostrar solo columnas relevantes para el usuario
        if all(col in df.columns for col in ['placa', 'tipo_vehiculo', 'hora_ingreso', 'id_usuario']):
            print(df[['placa', 'tipo_vehiculo', 'id_usuario', 'hora_ingreso']].to_string(index=False))
        else:
            print("Advertencia: Algunas columnas esperadas (placa, tipo_vehiculo, id_usuario, hora_ingreso) no se encontraron en parqueo.csv.")
            print(df.to_string(index=False)) # Imprime todo lo que tenga

def reporte_uso_frecuente():
    historial_path = DATA_DIR / "historial.csv"
    df = _load_csv_or_handle_error(historial_path, "reporte de uso frecuente")
    if df is None:
        return

    try:
        if df.empty or 'placa' not in df.columns:
            print("No hay datos suficientes o la columna 'placa' no existe para el reporte de uso frecuente.")
            return

        conteo = df['placa'].value_counts().head(5) # Top 5 vehículos
        print("\n--- Top 5 Vehículos más frecuentes ---")
        if conteo.empty:
            print("No hay registros de uso frecuentes para mostrar.")
        else:
            print(conteo.to_string(header=False)) # conteo ya tiene un nombre, no necesita cabecera extra
    except KeyError as e:
        print(f"ERROR: La columna 'placa' no se encontró en el historial para el reporte de uso frecuente: {e}")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al generar el reporte de uso frecuente: {e}")

def grafico_vehiculos_por_tipo():
    historial_path = DATA_DIR / "historial.csv"
    df = _load_csv_or_handle_error(historial_path, "gráfico de vehículos por tipo")
    if df is None:
        return

    try:
        if df.empty or 'tipo_vehiculo' not in df.columns:
            print("No hay datos suficientes o la columna 'tipo_vehiculo' no existe para el gráfico de tipos.")
            return
        
        conteo = df['tipo_vehiculo'].value_counts()
        if conteo.empty:
            print("No hay tipos de vehículos registrados para mostrar el gráfico.")
            return

        plt.figure(figsize=(8, 6)) # Tamaño de la figura
        conteo.plot(kind='bar', color='skyblue')
        plt.title("Distribución de Vehículos por Tipo (Historial)")
        plt.xlabel("Tipo de Vehículo")
        plt.ylabel("Cantidad de Registros")
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Añadir rejilla para mejor lectura
        plt.tight_layout()
        plt.show()
    except KeyError as e:
        print(f"ERROR: La columna 'tipo_vehiculo' no se encontró en el historial para el gráfico: {e}")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al generar el gráfico de vehículos por tipo: {e}")

def grafico_interactivo_tiempos_estadia():
    historial_path = DATA_DIR / "historial.csv"
    df = _load_csv_or_handle_error(historial_path, "gráfico interactivo de tiempos de estadía")
    if df is None:
        return

    try:
        # Verificar columnas antes de la conversión a datetime
        required_cols = ['hora_ingreso', 'hora_salida', 'placa'] # 'placa' para el hover
        if not all(col in df.columns for col in required_cols):
            print(f"No hay datos suficientes o faltan columnas de tiempo ({', '.join(required_cols)}) para el gráfico de estadía.")
            return

        df["hora_ingreso"] = pd.to_datetime(df["hora_ingreso"])
        df["hora_salida"] = pd.to_datetime(df["hora_salida"])
        
        # Filtro para asegurar que hora_salida sea siempre posterior o igual a hora_ingreso
        df = df[df["hora_salida"] >= df["hora_ingreso"]].copy() # Usar .copy() para evitar SettingWithCopyWarning

        # Calcular tiempo de estadía en horas para el histograma
        df["tiempo_estadia_horas"] = (df["hora_salida"] - df["hora_ingreso"]).dt.total_seconds() / 3600

        # Si no hay datos después de filtrar, salimos.
        if df.empty:
            print("No hay registros válidos de estadía (hora_salida >= hora_ingreso) para el gráfico.")
            return

        fig = px.histogram(df, x="tiempo_estadia_horas", nbins=20, 
                           title="Histograma de Tiempos de Estadía (Horas)",
                           labels={'tiempo_estadia_horas': 'Tiempo de Estadía (Horas)', 'count': 'Número de Vehículos'},
                           hover_data=['placa', 'hora_ingreso', 'hora_salida']) # Mostrar más info al pasar el mouse
        fig.update_layout(bargap=0.1)
        fig.show()

    except KeyError as e:
        print(f"ERROR: Faltan columnas esenciales ({e}) en el historial para el gráfico de tiempos de estadía.")
    except ValueError as e:
        print(f"ERROR: Formato de fecha/hora inválido en el historial. No se puede generar el gráfico de estadía: {e}")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al generar el gráfico interactivo de tiempos de estadía: {e}")

def reporte_ingresos_totales():
    historial_path = DATA_DIR / "historial.csv"
    df = _load_csv_or_handle_error(historial_path, "reporte de ingresos totales")
    if df is None:
        return

    try:
        if df.empty or 'valor_pagado' not in df.columns:
            print("No hay datos suficientes o la columna 'valor_pagado' no existe para el reporte de ingresos totales.")
            return

        # Convertir 'valor_pagado' a tipo numérico, manejando posibles errores
        df['valor_pagado'] = pd.to_numeric(df['valor_pagado'], errors='coerce')
        # Eliminar filas donde la conversión a numérico falló (quedaron como NaN)
        df.dropna(subset=['valor_pagado'], inplace=True)

        if df.empty:
            print("No hay registros de pagos válidos para calcular ingresos.")
            return

        ingresos_totales = df['valor_pagado'].sum()
        print("\n--- Reporte de Ingresos Totales ---")
        print(f"Ingresos totales generados: ${ingresos_totales:,.2f}") # Formatear como moneda

        # Opcional: Ingresos por tipo de vehículo (aunque para "solo carro" será un solo total)
        # ingresos_por_tipo = df.groupby('tipo_vehiculo')['valor_pagado'].sum()
        # if not ingresos_por_tipo.empty:
        #     print("\nIngresos por Tipo de Vehículo:")
        #     print(ingresos_por_tipo.to_string(header=False))

    except KeyError as e:
        print(f"ERROR: La columna 'valor_pagado' no se encontró en el historial para el reporte de ingresos totales: {e}")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al generar el reporte de ingresos totales: {e}")

def reporte_usuarios_registrados():
    usuarios_path = DATA_DIR / "usuarios.csv"
    df = _load_csv_or_handle_error(usuarios_path, "reporte de usuarios registrados")
    if df is None:
        return

    print("\n--- Usuarios Registrados ---")
    if df.empty:
        print("No hay usuarios registrados actualmente.")
    else:
        # Mostrar solo las columnas relevantes del usuario
        if all(col in df.columns for col in ['id', 'nombre', 'cedula', 'telefono', 'correo']):
            print(df[['id', 'nombre', 'cedula', 'telefono', 'correo']].to_string(index=False))
        else:
            print("Advertencia: Algunas columnas esperadas (id, nombre, cedula, telefono, correo) no se encontraron en usuarios.csv.")
            print(df.to_string(index=False)) # Imprime todo lo que tenga