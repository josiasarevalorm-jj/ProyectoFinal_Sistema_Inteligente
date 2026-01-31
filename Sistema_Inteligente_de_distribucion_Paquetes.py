archivoUsuario="usuarios.txt"
def registroUsuarios():
    global archivoUsuario
    print("\n--- REGUISTRO DE USUARIOS ---\n")
    nom=input("Ingrese su nombre: ")
    apell=input("Ingrese su apellido: ")
    identificacion=int(input("Ingrese su identidicacion: "))
    edad=int(input("ingrese su edad: "))
    usuario=f"{nom}.{apell}@gmail.com"
    print(f"Su usuario es: {usuario}")
    contraseña=input("Ingrese una contraseña: ")
    with open(archivoUsuario,"a") as archi:
        archi.write(f"{nom};{apell};{identificacion};{edad};{usuario};{contraseña}\n")

def menuAdministrador():
    while True:
        print("\n---ADMINISTRADOR---\n")
        print("1. Agregar nuevos centros de distribucion, rutas, distancias y costos.")
        print("2. Listar centros de rutas.")
        print("3. Consultar centro especifico.")
        print("4. Actualizar informacion de centros.")
        print("5. Eliminar centros o rutas.")
        print("6. Guaradar informacion en el archivo.")
        print("7. Salir.")
        opcion=int(input("Escoja una opcion: "))
        match opcion:
            case 1:
                print("### AGREGAR CENTROS ###")
            
            case 2:
                print("### LISTAR CENTROS ###")

            case 3:
                print("### CONSULTAR CENTRO ###")

            case 4:
                print("### ACTUALIZAR ###")

            case 5:
                print("### ELIMINAR ###")

            case 6:
                print("### GUARDAR EN ARCHIVO ###")

            case 7:
                print("Saiendo....")
                break
            case _:
                print("Ingrese una opcion valida.")

def menuCliente():
    while True:
        print("\n---CLIENTE---\n")
        print("1. Ver mapa de centros conectados.")
        print("2. Consultar la ruta optima.")
        print("3. Explorar centros organizados.")
        print("4. Selecionar centros de distribucion.")
        print("5. Listar centros selecionados y el costo total.")
        print("6. Actualizar selecion de centros.")
        print("7. Guardar la seleccion en un archivo.")
        print("8. Salir.")
        opcion=int(input("Elija una opcion: "))
        match opcion:
            case 1:
                print("### MAPA DE CENTROS CONECTADOS ###")
            
            case 2:
                print("### CONSULTAR LA RUTA MAS OPTIMA ###")

            case 3:
                print("### EXPLORAR CENTROS ORGANIZADOS ###")

            case 4: 
                print("### SELECIONAR CENTROS DE DISTRIBUCION ###")

            case 5:
                print("### LISTAR CENTROS Y COSTO TOTAL ###")

            case 6:
                print("### ACTUALIZAR SELECCION DE CENTROS ###")
            
            case 7:
                print("### GUARDAR EN EL ARCHIVO ###")

            case 8:
                print("Saliendo...")
                break
            case _:
                print("Elija una opcion valida")
    
registroUsuarios()