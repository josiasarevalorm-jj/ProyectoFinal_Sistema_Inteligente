import heapq
import os

USUARIOS_FILE = 'usuarios.txt'
CENTROS_FILE = 'centros.txt'
RUTAS_FILE = 'rutas.txt'

ADMIN_USUARIO = "admin@polidelivery.ec"
ADMIN_CONTRASENA = "AdminPoli2025!"
ADMIN_NOMBRES = "Administrador del Sistema"
ADMIN_IDEN = "9999999999"
ADMIN_EDAD = "99"

provincias = [
    {"nombre": "Pichincha", "capital": "Quito", "region": "Sierra"},
    {"nombre": "Guayas", "capital": "Guayaquil", "region": "Costa"},
    {"nombre": "Azuay", "capital": "Cuenca", "region": "Sierra"},
    {"nombre": "Tungurahua", "capital": "Ambato", "region": "Sierra"},
    {"nombre": "El Oro", "capital": "Machala", "region": "Costa"}
]

rutas_iniciales = [
    ("Quito", "Guayaquil", 420, 50.4),
    ("Quito", "Cuenca", 455, 54.6),
    ("Quito", "Ambato", 130, 15.6),
    ("Quito", "Machala", 480, 57.6),
    ("Guayaquil", "Cuenca", 195, 23.4),
    ("Guayaquil", "Ambato", 280, 33.6),
    ("Guayaquil", "Machala", 185, 22.2),
    ("Cuenca", "Ambato", 320, 38.4),
    ("Cuenca", "Machala", 150, 18.0),
    ("Ambato", "Machala", 380, 45.6),
]

if not os.path.exists(CENTROS_FILE):
    with open(CENTROS_FILE, 'w') as f:
        for p in provincias:
            f.write(f"{p['nombre']};{p['capital']};{p['region']}\n")

if not os.path.exists(RUTAS_FILE):
    with open(RUTAS_FILE, 'w') as f:
        for r in rutas_iniciales:
            f.write(f"{r[0]};{r[1]};{r[2]};{r[3]}\n")
            f.write(f"{r[1]};{r[0]};{r[2]};{r[3]}\n") 


def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return False
    has_lower = any(c.islower() for c in contrasena)
    has_upper = any(c.isupper() for c in contrasena)
    has_digit = any(c.isdigit() for c in contrasena)
    return has_lower and has_upper and has_digit

def cargar_usuarios():
    usuarios = {}
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 5:
                    usuario, contrasena, nombres, iden, edad = parts
                    usuarios[usuario] = {'contrasena': contrasena, 'nombres': nombres, 'iden': iden, 'edad': edad}
    return usuarios

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        for u, data in usuarios.items():
            f.write(f"{u}:{data['contrasena']}:{data['nombres']}:{data['iden']}:{data['edad']}\n")

def registrar_usuario():
    nombres = input("Nombres y Apellido: ")
    iden = input("Identificación: ")
    edad = input("Edad: ")
    usuario = f"{nombres.lower().replace(' ', '.')}@gmail.com"
    while True:
        contrasena = input("Contraseña segura: ")
        if validar_contrasena(contrasena):
            break
        print("Contraseña no segura. Debe tener minúsculas, mayúscula y número.")
    usuarios = cargar_usuarios()
    usuarios[usuario] = {'contrasena': contrasena, 'nombres': nombres, 'iden': iden, 'edad': edad}
    guardar_usuarios(usuarios)
    print("Registro exitoso.")
    return usuario

def iniciar_sesion():
    usuario = input("Usuario (email): ").strip()
    contrasena = input("Contraseña: ").strip()


    if usuario == ADMIN_USUARIO:
        if contrasena == ADMIN_CONTRASENA:
            print("\n→ Sesión iniciada como ADMINISTRADOR ←")
            return usuario, 'admin'
        else:
            print("Contraseña incorrecta para el administrador.")
            return None, None


    usuarios = cargar_usuarios()
    if usuario in usuarios and usuarios[usuario]['contrasena'] == contrasena:
        print(f"→ Sesión iniciada como CLIENTE ({usuarios[usuario]['nombres']}) ←")
        return usuario, 'cliente'

    print("Credenciales inválidas.")
    return None, None

def crear_admin_si_no_existe():
    usuarios = cargar_usuarios()
    
    if ADMIN_USUARIO not in usuarios:
        print(f"→ Creando cuenta de administrador por primera vez: {ADMIN_USUARIO}")
        usuarios[ADMIN_USUARIO] = {
            'contrasena': ADMIN_CONTRASENA,
            'nombres': ADMIN_NOMBRES,
            'iden': ADMIN_IDEN,
            'edad': ADMIN_EDAD
        }
        guardar_usuarios(usuarios)
        print("→ Administrador creado exitosamente ←\n")


def cargar_centros():
    centros = []
    if os.path.exists(CENTROS_FILE):
        with open(CENTROS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) == 3:
                    centros.append({"nombre": parts[0], "capital": parts[1], "region": parts[2]})
    return centros

def guardar_centros(centros):
    with open(CENTROS_FILE, 'w') as f:
        for c in centros:
            f.write(f"{c['nombre']};{c['capital']};{c['region']}\n")


def cargar_rutas():
    grafo = {}
    if os.path.exists(RUTAS_FILE):
        with open(RUTAS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) == 4:
                    origen, destino, dist, cost = parts
                    dist = float(dist)
                    cost = float(cost)
                    if origen not in grafo:
                        grafo[origen] = {}
                    grafo[origen][destino] = (dist, cost)
    return grafo

def guardar_rutas(grafo):
    with open(RUTAS_FILE, 'w') as f:
        for origen, dests in grafo.items():
            for destino, (dist, cost) in dests.items():
                f.write(f"{origen};{destino};{dist};{cost}\n")


def construir_matriz_costos(centros, grafo):
    n = len(centros)
    matriz = [[float('inf')] * n for _ in range(n)]
    nombre_to_idx = {c['capital']: i for i, c in enumerate(centros)}
    for i in range(n):
        matriz[i][i] = 0
    for origen, dests in grafo.items():
        if origen in nombre_to_idx:
            i = nombre_to_idx[origen]
            for destino, (dist, cost) in dests.items():
                if destino in nombre_to_idx:
                    j = nombre_to_idx[destino]
                    matriz[i][j] = cost
    return matriz


def dijkstra(grafo, inicio, fin):
    queue = [(0, inicio, [])]  
    visitados = set()
    while queue:
        costo, nodo, path = heapq.heappop(queue)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        path = path + [nodo]
        if nodo == fin:
            return path, costo
        if nodo in grafo:
            for vecino, (dist, cost) in grafo[nodo].items():
                if vecino not in visitados:
                    heapq.heappush(queue, (costo + cost, vecino, path))
    return None, float('inf')


def bfs(grafo, inicio):
    visitados = set()
    queue = [inicio]
    result = []
    while queue:
        nodo = queue.pop(0)
        if nodo not in visitados:
            visitados.add(nodo)
            result.append(nodo)
            if nodo in grafo:
                queue.extend(vecino for vecino in grafo[nodo] if vecino not in visitados)
    return result


def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(inicio)
    result = [inicio]
    if inicio in grafo:
        for vecino in grafo[inicio]:
            if vecino not in visitados:
                result.extend(dfs(grafo, vecino, visitados))
    return result


def construir_arbol(centros):
    arbol = {}
    for c in centros:
        region = c['region']
        if region not in arbol:
            arbol[region] = []
        arbol[region].append(c['capital'])
    return arbol


def burbuja(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def insercion(lista):
    for i in range(1, len(lista)):
        key = lista[i]
        j = i-1
        while j >= 0 and key < lista[j]:
            lista[j+1] = lista[j]
            j -= 1
        lista[j+1] = key
    return lista

def seleccion(lista):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if lista[min_idx] > lista[j]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista

def merge_sort(lista):
    if len(lista) > 1:
        mid = len(lista) // 2
        left = merge_sort(lista[:mid])
        right = merge_sort(lista[mid:])
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                lista[k] = left[i]
                i += 1
            else:
                lista[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            lista[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            lista[k] = right[j]
            j += 1
            k += 1
    return lista

def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    pivot = lista[len(lista)//2]
    left = [x for x in lista if x < pivot]
    middle = [x for x in lista if x == pivot]
    right = [x for x in lista if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def busqueda_lineal(lista, target):
    for i, item in enumerate(lista):
        if item == target:
            return i
    return -1

def busqueda_binaria(lista, target):
    low = 0
    high = len(lista) - 1
    while low <= high:
        mid = (low + high) // 2
        if lista[mid] == target:
            return mid
        elif lista[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def busqueda_interpolacion(lista, target):
    low = 0
    high = len(lista) - 1
    while low <= high and lista[low] <= target <= lista[high]:
        if low == high:
            if lista[low] == target:
                return low
            return -1
        pos = low + int(((high - low) / (lista[high] - lista[low])) * (target - lista[low]))
        if lista[pos] == target:
            return pos
        if lista[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1


def menu_admin(centros, grafo, matriz):
    while True:
        print("\nMenú Administrador:")
        print("1. Agregar centro")
        print("2. Listar centros (con ordenamiento)")
        print("3. Consultar centro (con búsqueda)")
        print("4. Actualizar centro")
        print("5. Eliminar centro")
        print("6. Agregar ruta")
        print("7. Salir")

        opcion = input("Opción: ")

        match opcion:

            case '1':
                nombre = input("Nombre provincia: ")
                capital = input("Capital: ")
                region = input("Región: ")
                centros.append({"nombre": nombre, "capital": capital, "region": region})
                guardar_centros(centros)

            case '2':
                lista_capitales = [c['capital'] for c in centros]
                print("Elige algoritmo: 1.Burbuja 2.Inserción 3.Selección 4.Merge 5.Quick")
                alg = input("Opción: ")

                match alg:
                    case '1':
                        sorted_list = burbuja(lista_capitales[:])
                    case '2':
                        sorted_list = insercion(lista_capitales[:])
                    case '3':
                        sorted_list = seleccion(lista_capitales[:])
                    case '4':
                        sorted_list = merge_sort(lista_capitales[:])
                    case '5':
                        sorted_list = quick_sort(lista_capitales[:])

                print("Centros ordenados:", sorted_list)

            case '3':
                target = input("Capital a buscar: ")
                lista_capitales = sorted([c['capital'] for c in centros])
                print("Elige algoritmo: 1.Lineal 2.Binaria 3.Interpolación")
                alg = input("Opción: ")

                match alg:
                    case '1':
                        idx = busqueda_lineal(lista_capitales, target)
                    case '2':
                        idx = busqueda_binaria(lista_capitales, target)
                    case '3':
                        idx = busqueda_interpolacion(lista_capitales, target)

                if idx != -1:
                    print("Encontrado:", centros[idx])
                else:
                    print("No encontrado.")

            case '4':
                capital = input("Capital a actualizar: ")
                for c in centros:
                    if c['capital'] == capital:
                        c['region'] = input("Nueva región: ")
                        break
                guardar_centros(centros)

            case '5':
                capital = input("Capital a eliminar: ")
                centros = [c for c in centros if c['capital'] != capital]

                for origen in list(grafo.keys()):
                    if origen == capital:
                        del grafo[origen]
                    else:
                        grafo[origen] = {d: v for d, v in grafo[origen].items() if d != capital}

                guardar_centros(centros)
                guardar_rutas(grafo)

            case '6':
                origen = input("Origen: ")
                destino = input("Destino: ")
                dist = float(input("Distancia: "))
                cost = float(input("Costo: "))

                if origen not in grafo:
                    grafo[origen] = {}
                grafo[origen][destino] = (dist, cost)

                if destino not in grafo:
                    grafo[destino] = {}
                grafo[destino][origen] = (dist, cost)

                guardar_rutas(grafo)

            case '7':
                break

            case _:
                print("Opción no válida.")



def menu_cliente(usuario, centros, grafo, matriz, arbol):
    seleccionados = []

    while True:
        print("\nMenú Cliente:")
        print("1. Ver mapa (grafo)")
        print("2. Consultar ruta óptima")
        print("3. Explorar jerarquía (árbol)")
        print("4. Seleccionar centros (mín 2)")
        print("5. Listar seleccionados (con ordenamiento)")
        print("6. Actualizar selección")
        print("7. Eliminar seleccionado")
        print("8. Guardar selección")
        print("9. Salir")

        opcion = input("Opción: ")

        match opcion:

            case '1':
                print("Mapa de conexiones:")
                for origen, dests in grafo.items():
                    for destino in dests:
                        print(f"{origen} -> {destino}")

            case '2':
                inicio = input("Inicio: ")
                fin = input("Fin: ")
                path, costo = dijkstra(grafo, inicio, fin)

                print("Ruta:", " -> ".join(path), "Costo:", costo)
                print("Sugerencia centros cercanos (BFS):", bfs(grafo, inicio))
                print("Exploración completa (DFS):", dfs(grafo, inicio))

            case '3':
                print("Jerarquía por regiones:")
                for region, caps in arbol.items():
                    print(f"{region}: {caps}")

            case '4':
                while len(seleccionados) < 2:
                    capital = input("Agregar capital: ")
                    if capital in [c['capital'] for c in centros]:
                        seleccionados.append(capital)
                    else:
                        print("No existe.")

            case '5':
                print("Elige algoritmo: 1.Burbuja 2.Inserción 3.Selección 4.Merge 5.Quick")
                alg = input("Opción: ")

                sorted_sel = seleccionados[:]

                match alg:
                    case '1':
                        burbuja(sorted_sel)
                    case '2':
                        insercion(sorted_sel)
                    case '3':
                        seleccion(sorted_sel)
                    case '4':
                        merge_sort(sorted_sel)
                    case '5':
                        sorted_sel = quick_sort(sorted_sel)

                costo_total = 0
                for i in range(len(sorted_sel)-1):
                    _, cost = dijkstra(grafo, sorted_sel[i], sorted_sel[i+1])
                    costo_total += cost

                print("Seleccionados ordenados:", sorted_sel, "Costo total:", costo_total)

            case '6':
                old = input("Capital a reemplazar: ")
                new = input("Nueva capital: ")
                if old in seleccionados:
                    seleccionados[seleccionados.index(old)] = new

            case '7':
                capital = input("Capital a eliminar: ")
                if capital in seleccionados:
                    seleccionados.remove(capital)

            case '8':
                nombre = usuario.split('@')[0].replace('.', '-')
                file = f"rutas-{nombre}.txt"
                with open(file, 'w') as f:
                    f.write("\n".join(seleccionados))
                print("Guardado en", file)

            case '9':
                break

            case _:
                print("Opción no válida.")


def main():
    crear_admin_si_no_existe()

    centros = cargar_centros()
    grafo = cargar_rutas()
    matriz = construir_matriz_costos(centros, grafo)
    arbol = construir_arbol(centros)

    while True:
        print("\n" + "="*50)
        print("       SISTEMA POLIDELIVERY - INICIO")
        print("="*50)
        print("1. Registrar nuevo cliente")
        print("2. Iniciar sesión")
        print("3. Salir")

        op = input("\nOpción → ").strip()

        match op:

            case '1':
                registrar_usuario()

            case '2':
                usuario, rol = iniciar_sesion()
                if usuario:
                    if rol == 'admin':
                        menu_admin(centros, grafo, matriz)
                    else:
                        menu_cliente(usuario, centros, grafo, matriz, arbol)

            case '3':
                print("\nGracias por usar PoliDelivery. ¡Hasta pronto!")
                break

            case _:
                print("Opción no válida.")


if __name__ == "__main__":
    main()