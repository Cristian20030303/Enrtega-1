#Validaciones de datos, Calculo de tarifas, fechas y tiempos y manejo de archivos

# Placa y entrada
def validar_placa(placa):
    return len(placa) == 6 and placa[:3].isalpha() and placa[3:].isdigit()

def timestamp_actual():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Tarifas
def calcular_tarifa(tipo, horas):
    if tipo == "carro":
        return 2000 * horas
    elif tipo == "moto":
        return 1000 * horas
    else:
        return 0

# 
