# Registro del usuario

import csv
from pathlib import Path
import sys 

# Importar funciones de utils alojadas en las en validaciones.py y helpers.oy
from utils.validaciones import validar_cedula, validar_correo_udea
from utils.helpers import usuario_registrado, generar_id_unico, limpiar_pantalla 

# Rutas a los archivos csv
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent 
DATA_DIR = project_root / "data"


def registrar_usuario():
    limpiar_pantalla()
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    
    users_file_path = DATA_DIR / "usuarios.csv" 

    while True:
        cedula = input("Ingrese la cédula del usuario (solo números): ").strip()
        if validar_cedula(cedula):
            if usuario_registrado(cedula, users_file_path): 
                print(f"La cédula {cedula} ya está registrada.")
                input("Presione Enter para continuar...")
                return 
            break 
        else:
            print("Cédula inválida. Debe ser numérica y tener entre 6 y 10 dígitos.")
            input("Presione Enter para continuar...")

    nombre = input("Ingrese el nombre completo del usuario: ").strip()
    telefono = input("Ingrese el teléfono del usuario (opcional): ").strip()
    while True:
        correo = input("Ingrese el correo electrónico del usuario (@udea.edu.co): ").strip()
        # Aquí se llama a la función de validación
        if validar_correo_udea(correo): 
            break # El correo es válido, salimos del bucle
        else:
            print("Correo inválido. Por favor, ingrese un correo que termine en @udea.edu.co")

    nuevo_id_usuario = generar_id_unico(users_file_path)
    
    if nuevo_id_usuario is None:
        input("Presione Enter para continuar...")
        return None, None, None 


    nuevo_usuario = {
        'id': nuevo_id_usuario,
        'nombre': nombre,
        'cedula': cedula,
        'telefono': telefono,
        'correo': correo
    }

    try:
        file_exists = users_file_path.exists() and users_file_path.stat().st_size > 0
        
        with open(users_file_path, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'nombre', 'cedula', 'telefono', 'correo']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader() 

            writer.writerow(nuevo_usuario)
        print("Usuario registrado exitosamente.")
        print(f"ID del nuevo usuario: {nuevo_id_usuario}") # Puedes añadir esto para verificar
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")
    
    input("Presione Enter para continuar...")
