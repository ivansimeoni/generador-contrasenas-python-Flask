from utils import *
from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal que muestra el formulario
@app.route('/')  # Cuando el usuario entra en la página principal "/"
def inicio():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    # Intenta leer el tamaño, usa 8 si no se escribió nada
    tamaño_str = request.form['tamaño']
    tamaño = int(tamaño_str) if tamaño_str else 8

    clave_generada = generar_contraseña(tamaño)
    # Muestra la clave generada y la pasa al form de guardar
    return render_template('index.html', clave=clave_generada)


# Ruta que guarda los datos del formulario
@app.route('/guardar', methods=['POST'])
def guardar():
    servicio = request.form['servicio']
    email = request.form['email']
    clave = request.form['clave']

    # Validar email
    valido, resultado = validar_email(email)
    if not valido:
        return f"Email no válido: {resultado}"
    # Si no hay clave (por ejemplo, el usuario no generó nada), se crea una por defecto
    if not clave:
        clave = generar_contraseña()
    
    token = encriptar_contraseña(clave)
    guardar_contraseña(token, servicio, resultado)
    # Mensaje de confirmación
    return f"Datos recibidos: {servicio}, {email}"

@app.route('/mostrar', methods=['GET'])
def mostrar():
    tabla = mostrar_contraseña()
    return render_template("index.html", tabla=tabla)
    

@app.route('/borrar', methods=['POST'])
def borrar():
    servicio = request.form['borrar'].strip().title()
    mensaje = eliminar_registro(servicio)
    return render_template('index.html',mensaje=mensaje )



if __name__ == '__main__':

    app.run(debug=True)

#http://localhost:5000