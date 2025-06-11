# URL local para acceder a la app
# http://localhost:5000
from utils import * # Importa todas las funciones auxiliares desde utils.py
from flask import Flask, render_template, request

app = Flask(__name__) 

# Ruta principal que muestra el formulario de inicio
@app.route('/')  # Cuando el usuario entra en la página principal "/"
def inicio():
    return render_template('index.html') 

# Ruta para generar una contraseña
@app.route('/generar', methods=['POST'])
def generar():
    # Lee el tamaño de la contraseña desde el formulario, usa 8 si está vacío
    tamaño_str = request.form['tamaño'].strip()
    tamaño = int(tamaño_str) if tamaño_str else 8

    clave_generada = generar_contraseña(tamaño)
    # Muestra la clave generada y la pasa al formulario para guardar
    return render_template('index.html', clave=clave_generada)

# Ruta que guarda los datos del formulario
@app.route('/guardar', methods=['POST'])
def guardar():
    # Obtiene y limpia los datos del formulario
    servicio = request.form['servicio'].strip().title()
    email = request.form['email'].strip()
    clave = request.form['clave'].strip()

    # Validar email
    valido, resultado = validar_email(email)
    if not valido:
        return f"Email no válido: {resultado}"
    # Si no hay clave, genera una por defecto
    if not clave:
        clave = generar_contraseña()
    
    token = encriptar_contraseña(clave)
    mensaje_guardar = guardar_contraseña(token, servicio, resultado)
    # Muestra mensaje de confirmación
    return render_template('index.html',mensaje_guardar=mensaje_guardar)

# Ruta para mostrar todas las contraseñas guardadas
@app.route('/mostrar', methods=['GET'])
def mostrar():
    tabla = mostrar_contraseña() # Obtiene la tabla de contraseñas
    return render_template("index.html", tabla=tabla)
    
# Ruta para borrar un registro por servicio
@app.route('/borrar', methods=['POST'])
def borrar():
    servicio = request.form['borrar'].strip().title() # Obtiene el servicio a borrar
    mensaje_borrar = eliminar_registro(servicio) # Elimina el registro
    return render_template('index.html',mensaje_borrar=mensaje_borrar )


if __name__ == '__main__':
    app.run(debug=True)
