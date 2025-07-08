# Perfil de administrador

# Importamos funciones desde visualizacion del archivo que existe en reportes.py
from visualizacion.reportes import reporte_uso_frecuente, reporte_ingresos_totales, reporte_vehiculos_activos, grafico_vehiculos_por_tipo, grafico_interactivo_tiempos_estadia, reporte_usuarios_registrados

# Importamos funciones de utils que existen de los archivos helpers.py y validaciones.py
from utils.helpers import limpiar_pantalla 
from utils.validaciones import validar_opcion 

def menu_administrador():
    opciones_validas = ["1", "2", "3", "4", "5", "6", "7"] 

    while True:
        limpiar_pantalla()
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Reporte de uso del parqueadero (Vehículos más frecuentes)")
        print("2. Reporte de vehículos activos") 
        print("3. Reporte de ingresos totales") 
        print("4. Reporte de usuarios registrados") 
        print("5. Gráfico interactivo de tiempos de estadía") 
        print("6. Volver al menú principal")  
        print("--------------------------")

        opcion = input("Seleccione una opción: ").strip() 

        if validar_opcion(opcion, opciones_validas): 
            if opcion == "1":
                reporte_uso_frecuente() 
            elif opcion == "2": 
                reporte_vehiculos_activos()
            elif opcion == "3": 
                reporte_ingresos_totales() 
            elif opcion == "4": 
                reporte_usuarios_registrados()
            elif opcion == "5": 
                grafico_interactivo_tiempos_estadia()
            elif opcion == "6":
                break 
        else:
            print("Opción inválida. Por favor, intente de nuevo.")
        
        input("\nPresione Enter para continuar...")
