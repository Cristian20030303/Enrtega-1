#Entrada y salida de vehiculos
vehiculos = []

def ingresar_vehiculo():
    placa = input("Placa: ").upper()
    tipo = input("Tipo (carro/moto): ").lower()
    entrada = timestamp_actual()
    vehiculos.append({"placa": placa, "tipo": tipo, "entrada": entrada})
