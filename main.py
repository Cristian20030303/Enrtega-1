# Menu principal



# main.py
import sys
from pathlib import Path

# --- Configuración de Rutas para Importaciones ---
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent # La raíz del proyecto es la carpeta donde está main.py

# Añade la raíz del proyecto al PYTHONPATH
# Esto permite importar 'src', 'utils' y 'visualizacion' como paquetes de nivel superior
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin Configuración de Rutas ---

# Importar funciones de los módulos usando su notación de paquete
try:
    from src.registro import registrar_usuario
    from src.ingreso import ingresar_vehiculo
    from src.retiro import retirar_vehiculo
    from src.administrador import menu_administrador
    
    # Importaciones de utils/ y validaciones/
    from utils.helpers import limpiar_pantalla # Esta sí existe y está definida
    from utils.validaciones import validar_opcion # Esta sí existe y está definida
    # Nota: Las funciones de reportes (visualizacion.reportes) se importan en administrador.py
    # No es necesario importarlas directamente aquí en main.py
except ImportError as e:
    print(f"Error al cargar un módulo esencial: {e}")
    print("Asegúrese de que todos los archivos .py estén en sus respectivas carpetas (src/, utils/, visualizacion/) y no contengan errores de sintaxis.")
    print("También, asegúrese de que existan archivos __init__.py vacíos en las carpetas 'src', 'utils' y 'visualizacion'.")
    sys.exit(1)

def menu_principal():
    opciones_validas = ["1", "2", "3", "4", "5"]

    while True:
        limpiar_pantalla()
        print("\n--- SISTEMA DE GESTIÓN DE PARQUEADERO UdeA ---")
        print("1. Registrar usuario")
        print("2. Ingresar vehículo")
        print("3. Retirar vehículo")
        print("4. Administrador")
        print("5. Salir")
        print("---------------------------------------")

        opcion = input("Seleccione una opción: ").strip()

        if validar_opcion(opcion, opciones_validas):
            if opcion == "1":
                registrar_usuario()
            elif opcion == "2":
                ingresar_vehiculo()
            elif opcion == "3":
                retirar_vehiculo()
            elif opcion == "4":
                menu_administrador()
            elif opcion == "5":
                print("Gracias por usar el sistema. ¡Hasta luego!")
                break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 5.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()