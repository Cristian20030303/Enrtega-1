#Registro de usuarios
usuarios = []

def registrar_usuario():
    nombre = input("Nombre del usuario: ").title().strip()
    documento = input("Documento: ").strip()
    usuarios.append({"nombre": nombre, "documento": documento})
