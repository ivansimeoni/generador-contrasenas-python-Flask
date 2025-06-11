
# Menú principal de opciones 
def menu_opciones(eleccion):
    

    if eleccion == 1:
        print("La contraseña debe tener al menos 8 caracteres.")
        tamaño = 0
        try:
            while True:
                tamaño = int(input("\n¿Cuántos caracteres quiere que tenga su contraseña? (solo números):\t").strip())
                if tamaño >= 8:
                    break
                else:
                    print("La contraseña debe tener al menos 8 caracteres.")
            clave_generada = generar_contraseña(tamaño)
            print(clave_generada)
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")
    
    elif eleccion == 2:

        print("Ingrese los datos del servicio que desea guardar:")
        nombre = input("\nNombre del servicio (ej: Gmail, Netflix):\t").strip().title()

        # Valida que el usuario sea un email válido
        while True:
            usuario = input("\nIngrese email asociado: \t").strip()
            control, resultado = validar_email(usuario)
            if control:
                break
            else:
                print(f"Email invalido: {resultado}")
        if len(clave_generada) <= 0:
            clave_generada = generar_contraseña()
        
        token = encriptar_contraseña(clave_generada)
        guardar_contraseña(token, nombre, resultado)

    elif eleccion == 3:
        mostrar_contraseña()
    
    elif eleccion == 4:




# Código principal
if __name__ == "__main__":
    print("Bienvenido a su gestor de contraseñas".upper())
    print("Aviso: la contraseña incluye letras mayúsculas, minúsculas, números y caracteres especiales")
    opcion = 0



    while opcion != 5:
        print("""\nQue tarea quieres realizar:
        \t1- Generar nueva contraseña
        \t2- Guardar contraseña
        \t3- Ver contraseñas almacenadas
        \t4- Eliminar registro
        \t5- Salir
        """)
        opcion = int(input("\n Ingrese el numero de la tarea a realizar\t").strip())

        menu_opciones(opcion)

        
