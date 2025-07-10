import re # Aquí usamos 're' para validar formatos específicos de texto, como la placa
# del carro o la cédula del usuario

def validar_placa(placa: str) -> bool:
    """
    Valida que la placa tenga exactamente 3 letras seguidas de 3 números.
    Ej: ABC123
    """
    # Expresión regular:
    # ^      : Inicio de la cadena
    # [A-Z]{3}: Exactamente 3 letras mayúsculas (A-Z)
    # \d{3}  : Exactamente 3 dígitos (0-9)
    # Lo utilizamos para que tome 3 letras y 3 numeros unica y exclusivamente especificando que es un carro
    pattern = r'^[A-Z]{3}\d{3}$'
    return re.fullmatch(pattern, placa.upper()) is not None # Convertimos a mayúsculas antes de validar

def validar_cedula(cedula: str) -> bool:
    """
    Verifica que la cédula sea numérica y tenga una longitud razonable (3 a 15 dígitos).
    Args:
        cedula (str): La cadena de la cédula a validar.
    Returns:
        bool: True si la cédula es válida, False en caso contrario.
    """
    if not isinstance(cedula, str):
        return False
    
    # Normalizamos la cédula quitando espacios antes de validar
    cedula_normalizada = cedula.strip()
    
    # isdigit() verifica que sean solo dígitos, y luego se revisa la longitud.
    return cedula_normalizada.isdigit() and 3 <= len(cedula_normalizada) <= 15

def validar_opcion(opcion: str, opciones_validas: list[str]) -> bool:
    """
    Valida si una opción ingresada está en una lista de opciones permitidas.
    Args:
        opcion (str): La opción ingresada por el usuario.
        opciones_validas (list[str]): Una lista de cadenas que representan las opciones permitidas.
    Returns:
        bool: True si la opción es válida, False en caso contrario.
    """
    if not isinstance(opcion, str):
        return False
    
    # Normalizamos la opción quitando espacios antes de comparar
    opcion_normalizada = opcion.strip()
    
    return opcion_normalizada in opciones_validas
def validar_correo_udea(correo: str) -> bool:
    """
    Valida que el correo electrónico tenga el formato correcto y termine en @udea.edu.co.
    Permite cualquier carácter (excepto espacio o @) en la parte del nombre de usuario.
    """
    # permite el registro de correos unica y exclusivamente para correos universitarios de la udea con todo tipo de signos
    pattern = r"^[^\s@]+@udea\.edu\.co$"
    
    print(f"DEBUG - Validando correo: '{correo}' con patrón: '{pattern}'")
    match = re.fullmatch(pattern, correo) 
    print(f"DEBUG - Resultado del match: {match}")
    return match is not None
