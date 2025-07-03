# Archivo principal del sistema de gestión de parqueadero
print("Bienvenido al sistema de parqueadero")
from src.gestion_usuarios import registrar_usuario
from src.vehiculos import ingresar_vehiculo
from src.reportes import generar_reporte

def main():
    # Aquí pruebas todo lo que vas desarrollando
    registrar_usuario()
    ingresar_vehiculo()
    generar_reporte()

if __name__ == "__main__":
    main()
