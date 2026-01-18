# Validación de edad agregada por [Santiago Nazareno Reyes]
import numpy as np

# ==========================================================
# 1. ENTIDAD DE DATOS Y LÓGICA INTERNA (Clase Estudiante) - CUMPLIENDO SRP
# ==========================================================

class Estudiante:
    """Clase de la Entidad Estudiante y su lógica interna (formato, promedio)."""

    def __init__(self, nombre: str, edad: int, notas: tuple):
        # Lógica de formato, encapsulada dentro de la clase
        self._nombre = self._formatear_nombre(nombre) 
        self.edad = edad
        # Almacenamiento eficiente de notas usando NumPy
        self.notas = np.array(notas) 

    @property
    def nombre(self):
        return self._nombre

    def _formatear_nombre(self, nombre):
        """Responsable solo del formato del nombre (SRP)."""
        return nombre.strip().title()

    def calcular_promedio(self):
        """Responsable solo de calcular el promedio (SRP)."""
        if self.notas.size == 0:
            return 0.0
        return self.notas.mean()

    def __str__(self):
        """Método de representación para la capa de presentación."""
        return f"Nombre: {self.nombre} | Edad: {self.edad} | Notas: {tuple(self.notas.tolist())} | Promedio: {self.calcular_promedio():.2f}"


# ==========================================================
# 2. REPOSITORIO DE DATOS (Clase RepositorioEstudiantes) - CUMPLIENDO OCP y DIP
# ==========================================================

class RepositorioEstudiantes:
    """Clase responsable SÓLO de la persistencia de datos (archivo I/O)."""
    
    def __init__(self, archivo_nombre="estudiantes.txt"):
        self.archivo_nombre = archivo_nombre

    def agregar(self, estudiante: Estudiante):
        """Escribe un objeto Estudiante en el archivo."""
        try:
            # Serializa el objeto a una línea de texto
            linea = f"{estudiante.nombre},{estudiante.edad},{estudiante.notas[0]},{estudiante.notas[1]},{estudiante.notas[2]}\n"
            with open(self.archivo_nombre, "a") as f:
                f.write(linea)
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")

    def leer_todos(self) -> list[Estudiante]:
        """Lee el archivo y deserializa las líneas en objetos Estudiante."""
        estudiantes = []
        try:
            with open(self.archivo_nombre, "r") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) == 5:
                        nombre = datos[0]
                        edad = int(datos[1])
                        notas = (float(datos[2]), float(datos[3]), float(datos[4]))
                        
                        # Crea la instancia de la clase (deserialización)
                        est = Estudiante(nombre, edad, notas) 
                        estudiantes.append(est)
        except FileNotFoundError:
            # Crea el archivo si no existe al intentar leer
            open(self.archivo_nombre, 'w').close() 
        except Exception as e:
             print(f"Error al leer datos: {e}")
             
        return estudiantes


# ==========================================================
# 3. LÓGICA DE NEGOCIO Y PRESENTACIÓN (Funciones de Alto Nivel)
# ==========================================================

def mostrar_mejor_estudiante(estudiantes: list[Estudiante]):
    """Responsable SÓLO de encontrar y presentar el mejor estudiante (SRP)."""
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return

    # Lógica de negocio
    mejor = max(estudiantes, key=lambda est: est.calcular_promedio())
    
    # Presentación
    print("\n--- Mejor Estudiante ---")
    print(f"🥇 El mejor estudiante es {mejor.nombre} con promedio {mejor.calcular_promedio():.2f}")


def mostrar_datos(estudiantes: list[Estudiante]):
    """Responsable SÓLO de la presentación de la lista (SRP)."""
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
        
    print("\n--- Listado de Estudiantes ---")
    for est in estudiantes:
        # Usa el método __str__ del objeto Estudiante para la presentación
        print(est) 

# ==========================================================
# 4. PROGRAMA PRINCIPAL (UI y Control de Flujo)
# ==========================================================

if __name__ == "__main__":
    # Inicialización: Se crea una instancia del Repositorio.
    repositorio = RepositorioEstudiantes()
    
    while True:
        print("\n--- Sistema de Gestión de Estudiantes ---")
        print("1. Agregar estudiante")
        print("2. Mostrar todos los estudiantes")
        print("3. Mostrar mejor estudiante")
        print("4. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            try:
                nombre = input("Nombre del estudiante: ")
                edad = int(input("Edad: "))
                notas = []
                for i in range(1, 4):
                    nota = float(input(f"Nota {i}: "))
                    notas.append(nota)
                
                # Crea el objeto (Lógica de Negocio)
                nuevo_estudiante = Estudiante(nombre, edad, tuple(notas))
                
                # Pide al Repositorio que persista el objeto (Persistencia)
                repositorio.agregar(nuevo_estudiante)
                print("✅ Estudiante agregado con éxito.")
            except ValueError:
                print("❌ Error: La edad y las notas deben ser números válidos.")
            
        elif opcion == "2":
            estudiantes = repositorio.leer_todos()
            mostrar_datos(estudiantes)
            
        elif opcion == "3":
            estudiantes = repositorio.leer_todos()
            mostrar_mejor_estudiante(estudiantes)
            
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
            
        else:
            print("Opción inválida, intenta de nuevo.")
