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

def main():
    crear_admin_si_no_existe()
    centros = cargar_centros()
    grafo = cargar_rutas()
    matriz = construir_matriz_costos(centros, grafo)
    arbol = construir_arbol(centros)

if __name__ == "__main__":
    main()


