# Perfil de administrador

# Importar funciones desde la carpeta visualizacion
from visualizacion.reportes import reporte_uso_frecuente, reporte_ingresos_totales, reporte_vehiculos_activos, reporte_total_vehiculos_registrados, grafico_interactivo_tiempos_estadia, reporte_usuarios_registrados, reporte_total_vehiculos_retirados, reporte_tiempo_promedio_estadia, reporte_tiempo_estadia_min_max, reporte_ocupacion_parqueadero

# Importar funciones de la carpeta de utils
from utils.helpers import limpiar_pantalla 
from utils.validaciones import validar_opcion 

# Definimos nuestro Menú Administrador
def menu_administrador():
    opciones_validas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"] 
# Definimos cada funcion que va a cumplir cada número
    while True:
        limpiar_pantalla()
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Reporte de uso del parqueadero (Vehículos más frecuentes)")
        print("2. Reporte de vehículos activos") 
        print("3. Reporte de ingresos totales") 
        print("4. Reporte de usuarios registrados") 
        print("5. Gráfico interactivo de tiempos de estadía") 
        print("6. Total de vehículos registrados")
        print("7. Total de vehículos retirados")
        print("8. Tiempo promedio de estadía por vehículo")
        print("9. Vehículo con tiempo de parqueo máximo y mínimo")
        print("10. Ocupación de celdas de parqueo")
        print("11. Volver al menú principal") # La opción de salida se mueve al final
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
                reporte_total_vehiculos_registrados()
            elif opcion == "7":
                reporte_total_vehiculos_retirados()
            elif opcion == "8":
                reporte_tiempo_promedio_estadia()
            elif opcion == "9":
                reporte_tiempo_estadia_min_max()
            elif opcion == "10":
                reporte_ocupacion_parqueadero()
            elif opcion == "11": # Opción de salida
                break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

        input("\nPresione Enter para continuar...")
