import string
import secrets
import sqlite3
from cryptography.fernet import Fernet
from pathlib import Path
from email_validator import validate_email, EmailNotValidError

# Creo la listas de variables con letras mayúsculas, minúsculas, números y caracteres especiales.
alfabeto = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

# Genera una contraseña segura con la longitud indicada por el usuario
def generar_contraseña(longitud=8):
    # Creo la listas de variables con letras mayúsculas, minúsculas, números y caracteres especiales.
    alfabeto = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alfabeto) for _ in range(longitud))
        # Verifica que la contraseña cumpla con los requisitos de seguridad,
        if (any(c.islower() for c in password) # Al menos una letra minúscula
                and any(c.isupper() for c in password) # Al menos una letra mayúscula
                and sum(c.isdigit() for c in password) >= 3 # Al menos tres números
                and sum(c in string.punctuation for c in password) >=2): # Al menos una 2 símbolos
            break
    return password

# Encripta la contraseña usando cifrado simétrica
def encriptar_contraseña(clave):
    try:
        # Lee la clave de encriptación desde un archivo
        with open(".key", "rb") as archivo:
            key = archivo.read()
        fernet = Fernet(key)
    except FileNotFoundError:
        # Si no existe la clave, crea el archivo, genera una nueva clave y la guarda
        key = Fernet.generate_key()
        with open(".key", "wb") as archivo:
            archivo.write(key)
        fernet = Fernet(key)

    clave_encriptado = fernet.encrypt(clave.encode())
    return clave_encriptado

# Desencripta la contraseña usando la clave almacenada
def desencriptar_contraseña(clave):
    try:
        with open(".key", "rb") as archivo:
            key = archivo.read()
        fernet = Fernet(key)
        clave_desencriptada = fernet.decrypt(clave)
        return clave_desencriptada
    except FileNotFoundError:
        None

# Guarda la contraseña encriptada junto con el nombre y usuario en la base de datos
def guardar_contraseña(token_encriptado, nombre, usuario):
    with sqlite3.connect("datos.db") as conexion:
        cursor = conexion.cursor()
        # Crea la tabla si no existe
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS claves (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Nombre TEXT,
                        Usuario TEXT,
                        Contraseña BINARY
                        )
        ''')
        # Inserta los datos en la tabla
        conexion.execute("insert into claves(Nombre, Usuario, Contraseña) values (?,?,?)", (nombre, usuario, token_encriptado))
        conexion.commit()
        
    
# Muestra todas las contraseñas almacenadas desencriptándolas
def mostrar_contraseña():
    # Comprueba que la base de datos existe
    if Path("datos.db").exists():
        with sqlite3.connect("datos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT Nombre, Usuario, Contraseña FROM claves")
            resultado = cursor.fetchall()

            datos = []
            for fila in range(0, len(resultado)):
                nombre = resultado[fila][0]
                usuario = resultado[fila][1]
                descifrado = desencriptar_contraseña(resultado[fila][2]).decode()
                datos.append((nombre, usuario, descifrado))
            return datos
    else:
        return []

# Valida que el email ingresado sea correcto
def validar_email(email):
    try:
        validar = validate_email(email, check_deliverability=True)
        return True, validar.normalized
    except EmailNotValidError as e:
        return False, e

# Elimina un registro de la base de datos
def eliminar_registro(identificador):
    if Path("datos.db").exists():
        with sqlite3.connect("datos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM claves WHERE Nombre = ?", (identificador, ))
            conexion.commit()
            
            if cursor.rowcount > 0:
                return "Registro del servicio eliminado."
            else:
                return "No se encontró ningún servicio con ese nombre."
    else:
        return "NO existen datos guardados. Por favor, cree y guarde una clave."