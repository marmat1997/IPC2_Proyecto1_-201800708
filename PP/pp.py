import xml.etree.ElementTree as ET


import xml.etree.ElementTree as ET
import subprocess




class Nodo:
    def __init__(self, matriz):
        self.matriz = matriz  # Objeto de tipo MatrizAcceso
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.puntero = None

    def agregar(self, matriz):
        nuevo_nodo = Nodo(matriz)
        if not self.puntero:
            self.puntero = nuevo_nodo
            self.puntero.siguiente = self.puntero
        else:
            actual = self.puntero
            while actual.siguiente != self.puntero:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.puntero

    def verificar(self, nombre):
        if not self.puntero:
            return False
        actual = self.puntero
        while True:
            if actual.matriz.nombre == nombre:
                return True
            actual = actual.siguiente
            if actual == self.puntero:
                break
        return False

    def mostrar_matrices(self):
        if not self.puntero:
            print("No hay matrices cargadas.")
            return
        actual = self.puntero
        while True:
            print(f"Matriz: {actual.matriz.nombre}")
            actual = actual.siguiente
            if actual == self.puntero:
                break

class MatrizAcceso:
    def __init__(self, nombre, n, m):
        self.nombre = nombre  # Nombre de la matriz
        self.n = n            # Número de filas
        self.m = m            # Número de columnas
    
    def agregar_dato(self, fila, columna, valor):
        setattr(self, f"dato_{fila}_{columna}", valor)
    
    def mostrar_matriz(self):
        for i in range(1, self.n + 1):
            fila = ""
            for j in range(1, self.m + 1):
                valor = getattr(self, f"dato_{i}_{j}", None)
                fila += f"{valor} " if valor is not None else "0 "
            print(fila)

def opcion1(ruta, lista_matrices):
    try:
        tree = ET.parse(ruta)
        root = tree.getroot()

        for matriz_element in root.findall('matriz'):
            nombre = matriz_element.get('nombre')
            n = int(matriz_element.get('n'))
            m = int(matriz_element.get('m'))
            
            if lista_matrices.verificar(nombre):
                print(f"La matriz '{nombre}' ya existe. No se puede agregar.")
                continue
            
            matriz = MatrizAcceso(nombre, n, m)

            for dato_element in matriz_element.findall('dato'):
                x = int(dato_element.get('x'))
                y = int(dato_element.get('y'))
                valor = int(dato_element.text)
                matriz.agregar_dato(x, y, valor)
            
            lista_matrices.agregar(matriz)
            print(f"Matriz '{nombre}' cargada con éxito.")
    
    except Exception as e:
        print(f"Error al cargar archivo: {e}")

def ProcesarArchivo(lista_matrices):
    print("Procesando archivo...")
    actual = lista_matrices.puntero
    if not actual:
        print("No hay matrices para procesar.")
        return
    while True:
        print(f"Procesando matriz: {actual.matriz.nombre}")
        actual.matriz.mostrar_matriz()
        actual = actual.siguiente
        if actual == lista_matrices.puntero:
            break

def escribir_archivo_salida(RutaSalida, lista_matrices):
    try:
        root = ET.Element("matrices_salida")
        actual = lista_matrices.puntero
        if not actual:
            print("No hay matrices para escribir.")
            return
        while True:
            matriz_salida = ET.SubElement(root, "matriz", nombre=f"{actual.matriz.nombre}_Salida", n=str(actual.matriz.n), m=str(actual.matriz.m))
            for i in range(1, actual.matriz.n + 1):
                for j in range(1, actual.matriz.m + 1):
                    valor = getattr(actual.matriz, f"dato_{i}_{j}", None)
                    ET.SubElement(matriz_salida, "dato", x=str(i), y=str(j)).text = str(valor)
            actual = actual.siguiente
            if actual == lista_matrices.puntero:
                break
        
        tree = ET.ElementTree(root)
        tree.write(RutaSalida)
        print(f"Archivo de salida guardado en {RutaSalida}")
    
    except Exception as e:
        print(f"Error al escribir archivo de salida: {e}")

def mostrar_datos_estudiante():
    print("Datos del estudiante:")
    print("Nombre: Piter Angel Esaù Valiente de León")
    print("Carné: 201902301")
    print("Curso: Seminario de Sistemas 2")
    print("Carrera: Ingeniería en Sistemas")
    print("Semestre: 2do semestre 2024")
    print("Documentación: https://linkdedocumentacion.com")

def generar_grafica(lista_matrices):
    if not lista_matrices.puntero:
        print("No hay matrices para graficar.")
        return

    dot = Digraph(comment='Matriz de Acceso')
    
    actual = lista_matrices.puntero
    while True:
        nombre_nodo = actual.matriz.nombre
        dot.node(nombre_nodo, nombre_nodo)
        
        # Crear relaciones entre matrices (en caso de que desees hacerlo)
        if actual.siguiente != lista_matrices.puntero:
            nombre_siguiente = actual.siguiente.matriz.nombre
            dot.edge(nombre_nodo, nombre_siguiente)

        actual = actual.siguiente
        if actual == lista_matrices.puntero:
            break
    
    dot.render('grafo_matriz_acceso', view=True)
    print("Gráfica generada y guardada como 'grafo_matriz_acceso.pdf'.")


def generate_dot(xml_data):
    root = ET.fromstring(xml_data)
    
    dot_code = 'digraph {\n'
    dot_code += '\tA [label="Matrices"]\n'
    
    node_counter = 1
    
    for matriz in root.findall('matriz'):
        m = matriz.get('m')
        n = matriz.get('n')
        nombre = matriz.get('nombre')
        matriz_label = f'{nombre} n = {n} m = {m}'
        
        dot_code += f'\tB [label="{matriz_label}"]\n'
        dot_code += '\tA -> B\n'
        
        for dato in matriz.findall('dato'):
            x = dato.get('x')
            y = dato.get('y')
            label = dato.text
            node_name = f'{node_counter}'
            dot_code += f'\t{node_name} [label={label}]\n'
            dot_code += f'\tB -> {node_name}\n'
            node_counter += 1
        
        # Optional: Reset node_counter for the next matrix if needed
        node_counter = 1

    dot_code += '}\n'
    return dot_code

def save_dot_file(dot_code, filename):
    with open(filename, 'w') as file:
        file.write(dot_code)

def generate_graph(image_file):
    subprocess.run(['dot', '-Tpng', 'matrices.dot', '-o', image_file])


def menu():
    lista_matrices = ListaCircular()
    while True:
        print("\nMenú Principal:")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo XML a cargar: ")
            opcion1(ruta, lista_matrices)
        elif opcion == "2":
            ProcesarArchivo(lista_matrices)
        elif opcion == "3":
            RutaSalida = input("Ingrese la ruta del archivo XML de salida: ")
            escribir_archivo_salida(RutaSalida, lista_matrices)
        elif opcion == "4":
            mostrar_datos_estudiante()
        elif opcion == "5":
            xml_file = input("Ingrese la ruta del archivo XML: ")
            with open(xml_file, 'r') as file:
                xml_data = file.read()
            
            dot_code = generate_dot(xml_data)
            dot_file = 'matrices.dot'
            image_file = 'matrices.png'
            
            save_dot_file(dot_code, dot_file)
            generate_graph(image_file)
            
            print(f'La gráfica ha sido generada y guardada en {image_file}')
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecución del menú
menu()