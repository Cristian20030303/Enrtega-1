import re # ¡IMPORTANTE: Añadir esta línea!

def validar_placa(placa: str) -> bool:
    """
    Valida que la placa tenga exactamente 3 letras seguidas de 3 números.
    Ej: ABC123
    """
    # Expresión regular:
    # ^      : Inicio de la cadena
    # [A-Z]{3}: Exactamente 3 letras mayúsculas (A-Z)
    # \d{3}  : Exactamente 3 dígitos (0-9)
    # $      : Fin de la cadena
    pattern = r'^[A-Z]{3}\d{3}$'
    return re.fullmatch(pattern, placa.upper()) is not None # Convertir a mayúsculas antes de validar

def validar_cedula(cedula: str) -> bool:
    """
    Verifica que la cédula sea numérica y tenga una longitud razonable (6 a 10 dígitos).
    Args:
        cedula (str): La cadena de la cédula a validar.
    Returns:
        bool: True si la cédula es válida, False en caso contrario.
    """
    if not isinstance(cedula, str):
        return False
    
    # Normalizar la cédula (quitar espacios) antes de validar
    cedula_normalizada = cedula.strip()
    
    # isdigit() verifica que sean solo dígitos, y luego se revisa la longitud.
    return cedula_normalizada.isdigit() and 6 <= len(cedula_normalizada) <= 10

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
    
    # Normalizar la opción (quitar espacios) antes de comparar
    opcion_normalizada = opcion.strip()
    
    return opcion_normalizada in opciones_validas
def validar_correo_udea(correo: str) -> bool:
    """
    Valida que el correo electrónico tenga el formato correcto y termine en @udea.edu.co.
    Permite cualquier carácter (excepto espacio o @) en la parte del nombre de usuario.
    """
    # Nueva expresión regular más permisiva para la parte del usuario
    # [^\s@]+ : Coincide con uno o más caracteres que NO sean un espacio en blanco (\s) o un arroba (@).
    # @udea\.edu\.co$: El dominio sigue siendo estricto y escapado.
    pattern = r"^[^\s@]+@udea\.edu\.co$"
    
    print(f"DEBUG - Validando correo: '{correo}' con patrón: '{pattern}'")
    match = re.fullmatch(pattern, correo) # re.UNICODE ya no es tan crítico aquí si permitimos casi todo
    print(f"DEBUG - Resultado del match: {match}")
    return match is not None