import time
from collections import deque

# ---------------------------------------------------------
# Clase Proceso: Representa la unidad básica de trabajo
# ---------------------------------------------------------
class Proceso:
    def __init__(self, nombre, tiempo):
        # Inicialización de atributos del proceso
        self.nombre = nombre
        self.tiempo_total = tiempo
        self.tiempo_restante = tiempo
        self.estado = "Listo"  # Estados: Listo, Ejecutando, Terminado

    def __str__(self):
        # Formato de impresión para la tabla de procesos
        return f"{self.nombre.ljust(10)} | Restante: {str(self.tiempo_restante).zfill(2)}s | Estado: {self.estado}"


# ---------------------------------------------------------
# Clase SistemaOperativo: Gestiona la lógica y planificación
# ---------------------------------------------------------
class SistemaOperativo:
    def __init__(self):
        # Lista global para almacenar todos los procesos creados
        self.procesos = []

    # Método para dar de alta nuevos procesos en el sistema
    def crear_proceso(self):
        try:
            nombre = input("Nombre del proceso: ")
            tiempo = int(input("Tiempo de ejecución (segundos): "))
            nuevo = Proceso(nombre, tiempo)
            self.procesos.append(nuevo)
            print(f"Proceso '{nombre}' creado satisfactoriamente.\n")
        except ValueError:
            print("Error: El tiempo debe ser un valor numerico entero.\n")

    # Método para visualizar el estado actual de todos los procesos
    def mostrar_procesos(self):
        if not self.procesos:
            print("\n[ No hay procesos registrados en el sistema ]\n")
            return
        
        print("\n--- TABLA DE CONTROL DE PROCESOS ---")
        for p in self.procesos:
            print(p)
        print("------------------------------------\n")

    # Método para remover un proceso de la lista por su nombre
    def eliminar_proceso(self):
        nombre = input("Nombre del proceso a eliminar: ")
        original_count = len(self.procesos)
        # Filtramos la lista para excluir el proceso con el nombre indicado
        self.procesos = [p for p in self.procesos if p.nombre != nombre]
        
        if len(self.procesos) < original_count:
            print(f"Proceso '{nombre}' eliminado del sistema.\n")
        else:
            print(f"Error: No se encontro el proceso '{nombre}'.\n")

    # Algoritmo de Planificacion: First Come, First Served (FCFS)
    def ejecutar_fcfs(self):
        if not self.procesos:
            print("No hay procesos pendientes.")
            return

        print("\nIniciando planificacion FCFS...")
        for p in self.procesos:
            # Ignorar procesos que ya fueron completados previamente
            if p.estado == "Terminado": continue
            
            p.estado = "Ejecutando"
            print(f"Atendiendo {p.nombre}... ({p.tiempo_restante}s)")
            
            # El proceso ocupa la CPU hasta que termina su tiempo total
            time.sleep(1) 
            p.tiempo_restante = 0
            p.estado = "Terminado"
            print(f"Proceso {p.nombre} finalizado.")

        print("\nCiclo de ejecucion FCFS concluido.\n")

    # Algoritmo de Planificacion: Round Robin (RR)
    def ejecutar_rr(self):
        if not self.procesos:
            print("No hay procesos pendientes.")
            return

        try:
            quantum = int(input("Defina el valor del Quantum (tiempo por turno): "))
        except ValueError:
            print("Error: El quantum debe ser un numero entero.")
            return

        # Creamos una cola de ejecucion solo con los procesos que no han terminado
        cola_rr = deque([p for p in self.procesos if p.estado != "Terminado"])
        
        print(f"\nIniciando planificacion Round Robin (Quantum: {quantum})...")
        
        while cola_rr:
            # Extraemos el primer proceso de la cola
            p = cola_rr.popleft() 
            p.estado = "Ejecutando"
            
            # Se ejecuta el minimo entre lo que le queda y el quantum permitido
            tiempo_a_ejecutar = min(p.tiempo_restante, quantum)
            print(f"Ejecutando {p.nombre} por {tiempo_a_ejecutar}s...", end=" ", flush=True)
            
            time.sleep(1) 
            p.tiempo_restante -= tiempo_a_ejecutar
            
            # Si todavia le queda tiempo, regresa al final de la cola
            if p.tiempo_restante > 0:
                p.estado = "Listo"
                print(f"Regresa a cola (faltan {p.tiempo_restante}s)")
                cola_rr.append(p)
            else:
                p.estado = "Terminado"
                print("Finalizado.")

        print("\nCiclo Round Robin completado.\n")

    # Interfaz de usuario tipo terminal
    def menu(self):
        while True:
            print("======== SISTEMA OPERATIVO SIMULACION ========")
            print("1. Crear proceso")
            print("2. Ver procesos")
            print("3. Eliminar proceso")
            print("4. Ejecutar FCFS")
            print("5. Ejecutar Round Robin")
            print("6. Salir")
            print("==============================================")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1": self.crear_proceso()
            elif opcion == "2": self.mostrar_procesos()
            elif opcion == "3": self.eliminar_proceso()
            elif opcion == "4": self.ejecutar_fcfs()
            elif opcion == "5": self.ejecutar_rr()
            elif opcion == "6":
                print("Apagando el sistema..."); break
            else:
                print("Opcion no reconocida. Reintente.\n")

# ---------------------------------------------------------
# Punto de entrada del programa
# ---------------------------------------------------------
if __name__ == "__main__":
    sistema = SistemaOperativo()
    sistema.menu()