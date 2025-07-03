#Registro, ingreso retiro y administrador
from src.registro import registrar_usuario
from src.ingreso import ingresar_vehiculo
from src.retiro import retirar_vehiculo
from src.administrador import menu_administrador

def menu():
    while True:
        print("\n--- PARQUEADERO EL OLVIDO ---")
        print("1. Registrar usuario")
        print("2. Ingresar vehículo")
        print("3. Retirar vehículo")
        print("4. Acceder como administrador")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            ingresar_vehiculo()
        elif opcion == '3':
            retirar_vehiculo()
        elif opcion == '4':
            menu_administrador()
        elif opcion == '5':
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
