# tarifas.py

# tarifas.py

def calcular_tarifa(tiempo_minutos: int | float, tipo_vehiculo: str) -> float:
    """
    Calcula el valor a pagar por el parqueadero.
    Este parqueadero está configurado para manejar **solo vehículos tipo 'carro'**.

    Args:
        tiempo_minutos (int | float): El tiempo de estadía en minutos.
        tipo_vehiculo (str): El tipo de vehículo (debe ser 'carro').

    Returns:
        float: El valor total a pagar.

    Raises:
        TypeError: Si 'tiempo_minutos' no es un valor numérico.
        ValueError: Si el 'tipo_vehiculo' no es 'carro' o si el tiempo es negativo.
    """
    # 1. Validar el tipo de vehículo estrictamente para "carro"
    tipo_vehiculo_lower = tipo_vehiculo.lower().strip() # Añadido .strip() para mayor robustez
    if tipo_vehiculo_lower != "carro":
        raise ValueError(f"Este parqueadero es exclusivo para 'carros'. Tipo de vehículo '{tipo_vehiculo}' no permitido.")

    # 2. Definir la tarifa por minuto para carros
    tarifa_minuto_carro = 100 

    # 3. Validar que tiempo_minutos sea numérico
    if not isinstance(tiempo_minutos, (int, float)):
        raise TypeError(f"El tiempo_minutos debe ser un valor numérico (entero o flotante). Recibido: {type(tiempo_minutos).__name__}")
    
    # 4. Validar que el tiempo_minutos no sea negativo
    if tiempo_minutos < 0:
        raise ValueError("El tiempo de estadía no puede ser negativo.")

    # 5. Calcular y retornar la tarifa
    # Opcional: Si quieres redondear a enteros para montos de dinero:
    # return float(round(tiempo_minutos * tarifa_minuto_carro))
    # O si quieres un número específico de decimales (ej. 2):
    # return round(float(tiempo_minutos * tarifa_minuto_carro), 2)
    return float(tiempo_minutos * tarifa_minuto_carro)