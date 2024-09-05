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
            print("algo aca")
            #opcion5()

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
        print("Bandera")
        for i in range(1, self.n + 1):
            fila = ""
            for j in range(1, self.m + 1):
                valor = getattr(self, f"dato_{i}_{j}", None)
                fila += f"{valor} " if valor is not None else "0 "
            print(fila)

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
        self.matriz = matriz  # Objeto de tipo MatrizAcceso
        self.siguiente = None

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




if __name__ == "__main__":
    main()