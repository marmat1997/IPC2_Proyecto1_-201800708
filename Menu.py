import xml.etree.ElementTree as ET
import subprocess

def MostrarMenu():
    print("1. Cargar Archivo")
    print("2. Procesar Archivo")
    print("3. Escribir archivo de salida")
    print("4. Datos del Estudiante")
    print("5. Generar Gráfica")
    print("6. Salir")
    print("7. Mostrar autos")


def opcion4():
    print("Marvin Enrique Ajquejay Matias\n")
    print("201800708\n")
    
def main():
    lista_matrices = ListaCircular()
    conteo=0
    while True:
        MostrarMenu()
        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            ruta_archivo = input("Ingrese la ruta del archivo XML a cargar: ")
            opcion1(ruta_archivo, lista_matrices)
            
        elif opcion == "7":
            opcion7()
        elif opcion == "6":
            print("adios")
            break
        elif opcion == "2":
            ProcesarArchivo(lista_matrices)
        elif opcion == "8":
            opcion8()
        elif opcion =="3":
            Compra()
        elif opcion =="4":
            opcion4()
        elif opcion =="5":
            if lista_matrices.puntero is not None:
                actual = lista_matrices.puntero
                while True:
                    print(f"Generando gráfica de la matriz: {actual.matriz.nombre}")
                    actual.matriz.Graficar_matriz()
                    actual = actual.siguiente
                    if actual == lista_matrices.puntero:
                        break
            else:
                print("No hay matrices cargadas para graficar.")

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

class MatrizAcceso:
    def __init__(self, nombre, n, m):
        self.nombre = nombre  # Nombre de la matriz
        self.n = n            # Número de filas
        self.m = m            # Número de columnas
    
    def agregar_dato(self, fila, columna, valor):
        setattr(self, f"dato_{fila}_{columna}", valor)
    
    def mostrar_matriz(self):
        ##print("Bandera")
        for i in range(1, self.n + 1):
            fila = ""
            for j in range(1, self.m + 1):
                valor = getattr(self, f"dato_{i}_{j}", None)
                fila += f"{valor} " if valor is not None else "0 "
            print(fila)

    def Graficar_matriz(self):
        # Crear el archivo dot para Graphviz
        nombre_archivo_dot = f"{self.nombre}.dot"
        with open(nombre_archivo_dot, "w") as file:
            file.write("digraph G {\n")
            file.write("  rankdir=TB;\n")  # Dirección de arriba hacia abajo
            file.write("  node [shape=ellipse];\n")

            # Crear el nodo raíz
            file.write(f'  "Matrices" [label="Matrices", shape=ellipse];\n')
            file.write(f'  "{self.nombre}" [label="{self.nombre}", shape=ellipse];\n')
            file.write(f'  "Matrices" -> "{self.nombre}";\n')

            # Crear nodos para n y m (filas y columnas)
            file.write(f'  "n" [label="n={self.n}", shape=circle, color=blue, style=filled];\n')
            file.write(f'  "m" [label="m={self.m}", shape=circle, color=blue, style=filled];\n')
            file.write(f'  "{self.nombre}" -> "n";\n')
            file.write(f'  "{self.nombre}" -> "m";\n')

            # Crear nodos y conexiones para la matriz
            for j in range(1, self.m + 1):
                #file.write(f'  "col_{j}" [label="", shape=ellipse];\n')
                #file.write(f'  "{self.nombre}" -> "col_{j}";\n')
                for i in range(1, self.n + 1):
                    valor = getattr(self, f"dato_{i}_{j}", 0)
                    file.write(f'  "celda_{i}_{j}" [label="{valor}", shape=ellipse];\n')
                    if i == 1:
                        file.write(f'  "{self.nombre}" -> "celda_{i}_{j}";\n')
                    else:
                        file.write(f'  "celda_{i-1}_{j}" -> "celda_{i}_{j}";\n')

            file.write("}\n")

        # Ejecutar el comando para generar la imagen usando Graphviz
        try:
            subprocess.run(["dot", "-Tpng", nombre_archivo_dot, "-o", f"{self.nombre}.png"])
            print(f"Gráfica generada como {self.nombre}.png")
        except Exception as e:
            print(f"Error al generar la gráfica: {e}")

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

class Nodo:
    def __init__(self, matriz):
        self.matriz = matriz  
        self.siguiente = None

def ProcesarArchivo(lista_matrices):
    actual = lista_matrices.puntero
    if not actual:
        print("No hay matrices para procesar.")
        return

    while True:
        matriz = actual.matriz
        print(f"\nProcesando matriz: {matriz.nombre}")
        matriz.mostrar_matriz()

        # MatrizAcceso para almacenar patrones de acceso (usamos dos columnas, una para el patrón y otra para la fila)
        patrones_acceso = MatrizAcceso("PatronesAcceso", matriz.n, 2)

        # Crear una matriz para las sumas por patrón (número de filas igual al número de patrones que encontremos)
        sumas_por_patron = MatrizAcceso("SumasPorPatron", 0, matriz.m)  # Inicialmente 0 filas, m columnas

        numero_patrones = 0  # Contador de patrones únicos

        for i in range(1, matriz.n + 1):
            patron_binario = ""
            suma_fila = MatrizAcceso(f"SumaFila_{i}", 1, matriz.m)  # MatrizAcceso en lugar de lista para las sumas por fila

            for j in range(1, matriz.m + 1):
                valor = getattr(matriz, f"dato_{i}_{j}", 0)
                patron_binario += "1" if valor > 0 else "0"  # Crear el patrón binario basado en los valores de la fila
                suma_fila.agregar_dato(1, j, valor)  # Guardar el valor en la "matriz" suma_fila

            # Buscar si el patrón ya existe en patrones_acceso
            patron_existe = False
            for k in range(1, numero_patrones + 1):
                if getattr(patrones_acceso, f"dato_{k}_1") == patron_binario:
                    patron_existe = True
                    # Actualizar la suma de ese patrón
                    for j in range(1, matriz.m + 1):
                        valor_actual = getattr(sumas_por_patron, f"dato_{k}_{j}", 0)
                        nuevo_valor = valor_actual + getattr(suma_fila, f"dato_1_{j}", 0)
                        sumas_por_patron.agregar_dato(k, j, nuevo_valor)
                    break

            if not patron_existe:
                # Si el patrón no existe, lo agregamos a patrones_acceso y sumas_por_patron
                numero_patrones += 1
                patrones_acceso.agregar_dato(numero_patrones, 1, patron_binario)
                patrones_acceso.agregar_dato(numero_patrones, 2, i)  # Guardamos la fila asociada al patrón

                # Expandimos sumas_por_patron agregando una nueva fila
                sumas_por_patron.n = numero_patrones
                for j in range(1, matriz.m + 1):
                    sumas_por_patron.agregar_dato(numero_patrones, j, getattr(suma_fila, f"dato_1_{j}", 0))

        # Mostrar los patrones y las sumas
        print(f"Patrones de acceso para la matriz '{matriz.nombre}':")
        for k in range(1, numero_patrones + 1):
            patron = getattr(patrones_acceso, f"dato_{k}_1")
            fila_asociada = getattr(patrones_acceso, f"dato_{k}_2")
            print(f"Patrón {patron}: Tupla {fila_asociada}, Suma:", end=" ")
            for j in range(1, matriz.m + 1):
                print(getattr(sumas_por_patron, f"dato_{k}_{j}", 0), end=" ")
            print()

        actual = actual.siguiente
        if actual == lista_matrices.puntero:
            break

if __name__ == "__main__":
    main()