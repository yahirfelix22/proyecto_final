mport time #importa la libreria time para simular el paso del tiempo en la ejecución de procesos
from collections import deque #| Importa deque para implementar la cola del algoritmo Round Robin

# ---------------------------------------------------------
# Clase de Colores para una Interfaz Profesional
# ---------------------------------------------------------
class Color:
    VERDE = '\033[92m'    # Ejecutando / Éxito
    AMARILLO = '\033[93m' # Listo / Advertencia
    ROJO = '\033[91m'     # Terminado / Errores
    CYAN = '\033[96m'     # Títulos / Menú
    BLANCO = '\033[97m'   # Texto resaltado
    RESET = '\033[0m'     # Resetear color

# ---------------------------------------------------------
# Clase Proceso: Representa la unidad básica de trabajo [cite: 5, 18, 23]
# ---------------------------------------------------------
class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo_total = tiempo
        self.tiempo_restante = tiempo
        self.estado = "Listo"  # Estados: Listo, Ejecutando, Terminado [cite: 22, 25, 26, 27]

    def __str__(self):
        # Asignar color según el estado para mayor claridad visual
        color_estado = Color.AMARILLO
        if self.estado == "Ejecutando": color_estado = Color.VERDE
        elif self.estado == "Terminado": color_estado = Color.ROJO
        
        estado_fmt = f"{color_estado}{self.estado.ljust(10)}{Color.RESET}"
        return f"{Color.BLANCO}{self.nombre.ljust(12)}{Color.RESET} | Restante: {str(self.tiempo_restante).zfill(2)}s | Estado: {estado_fmt}"

# ---------------------------------------------------------
# Clase SistemaOperativo: Gestiona la lógica y planificación [cite: 15]
# ---------------------------------------------------------
class SistemaOperativo:
    def __init__(self):
        self.procesos = []

    def crear_proceso(self):
        try:
            nombre = input(f"{Color.CYAN}Nombre del proceso: {Color.RESET}")
            tiempo = int(input(f"{Color.CYAN}Tiempo de ejecución (segundos): {Color.RESET}"))
            nuevo = Proceso(nombre, tiempo)
            self.procesos.append(nuevo)
            print(f"{Color.VERDE}✔ Proceso '{nombre}' creado satisfactoriamente.{Color.RESET}\n")
        except ValueError:
            print(f"{Color.ROJO}✘ Error: El tiempo debe ser un valor numérico entero.{Color.RESET}\n")
#crea un proceso solicitando al usuario el nombre y el tiempo de ejecución, luego lo agrega a la lista de procesos del sistema operativo. 
#Si el usuario ingresa un valor no numérico para el tiempo, se muestra un mensaje de error.
# ---------------------------------------------------------

    def mostrar_procesos(self):
        if not self.procesos:
            print(f"\n{Color.AMARILLO}[ No hay procesos registrados ]{Color.RESET}\n")
            return
        
        print(f"\n{Color.CYAN}┌──────────────────────────────────────────────────────────┐")
        print(f"│            TABLA DE CONTROL DE PROCESOS (PCB)            │")
        print(f"└──────────────────────────────────────────────────────────┘{Color.RESET}")
        for p in self.procesos:
            print(f"  {p}")
        print(f"{Color.CYAN}────────────────────────────────────────────────────────────{Color.RESET}\n")

    def eliminar_proceso(self):
        nombre = input(f"{Color.CYAN}Nombre del proceso a eliminar: {Color.RESET}")
        original_count = len(self.procesos)
        self.procesos = [p for p in self.procesos if p.nombre != nombre]
        
        if len(self.procesos) < original_count:
            print(f"{Color.VERDE}✔ Proceso '{nombre}' eliminado.{Color.RESET}\n")
        else:
            print(f"{Color.ROJO}✘ Error: No se encontró el proceso '{nombre}'.{Color.RESET}\n")

    # Algoritmo FCFS [cite: 30]
    def ejecutar_fcfs(self):
        if not self.procesos:
            print(f"{Color.ROJO}No hay procesos para ejecutar.{Color.RESET}")
            return

        print(f"\n{Color.VERDE}▶ Iniciando FCFS...{Color.RESET}")
        for p in self.procesos:
            if p.estado == "Terminado": continue
            
            p.estado = "Ejecutando"
            print(f"  {Color.VERDE}●{Color.RESET} Atendiendo {p.nombre} ({p.tiempo_restante}s)...", end="\r")
            
            # Simulación de tiempo real [cite: 38, 42]
            for _ in range(p.tiempo_restante):
                time.sleep(0.5) # Ajustado para que la simulación no sea eterna
            
            p.tiempo_restante = 0
            p.estado = "Terminado"
            print(f"  {Color.VERDE}✔{Color.RESET} Proceso {p.nombre} finalizado.             ")

        print(f"{Color.VERDE}Planificación FCFS concluida.{Color.RESET}\n")

    # Algoritmo Round Robin [cite: 31]
    def ejecutar_rr(self):
        if not [p for p in self.procesos if p.estado != "Terminado"]:
            print(f"{Color.ROJO}No hay procesos pendientes.{Color.RESET}")
            return

        try:
            quantum = int(input(f"{Color.CYAN}Defina el Quantum (segundos): {Color.RESET}"))
        except ValueError:
            print(f"{Color.ROJO}Error: El quantum debe ser un número entero.{Color.RESET}")
            return

        cola_rr = deque([p for p in self.procesos if p.estado != "Terminado"])
        print(f"\n{Color.VERDE}▶ Iniciando Round Robin (Q={quantum})...{Color.RESET}")
        
        while cola_rr:
            p = cola_rr.popleft()
            p.estado = "Ejecutando"
            
            tiempo_a_ejecutar = min(p.tiempo_restante, quantum)
            print(f"  {Color.VERDE}⚡{Color.RESET} {p.nombre} por {tiempo_a_ejecutar}s...", end=" ", flush=True)
            
            time.sleep(1) 
            p.tiempo_restante -= tiempo_a_ejecutar
            
            if p.tiempo_restante > 0:
                p.estado = "Listo"
                print(f"{Color.AMARILLO}↩ Regresa a cola{Color.RESET}")
                cola_rr.append(p)
            else:
                p.estado = "Terminado"
                print(f"{Color.VERDE}✔ Finalizado{Color.RESET}")

        print(f"{Color.VERDE}Ciclo Round Robin completado.{Color.RESET}\n")
# La función ejecutar_rr implementa el algoritmo de planificación Round Robin, donde se solicita al usuario el quantum (tiempo máximo que cada proceso puede ejecutarse antes de ceder el CPU).
# Se utiliza una cola (deque) para gestionar los procesos que están listos para ejecutarse. 
# Cada proceso se ejecuta por un tiempo determinado (el mínimo entre su tiempo restante y el quantum), y luego se actualiza su estado y tiempo restante. 
# Si el proceso no ha terminado, se vuelve a colocar al final de la cola; de lo contrario, se marca como terminado.
    # Interfaz tipo terminal [cite: 32, 37]
#----------------------------------------------------------
    def menu(self):
        while True:
            print(f"{Color.CYAN}╔════════════════════════════════════════════╗")
            print(f"║     SIMULACIÓN DE SISTEMA OPERATIVO        ║")
            print(f"╠════════════════════════════════════════════╣")
            print(f"║ {Color.BLANCO}1. Crear proceso{Color.CYAN}                           ║")
            print(f"║ {Color.BLANCO}2. Ver procesos (PCB){Color.CYAN}                      ║")
            print(f"║ {Color.BLANCO}3. Eliminar proceso{Color.CYAN}                        ║")
            print(f"║ {Color.BLANCO}4. Ejecutar Planificador FCFS{Color.CYAN}              ║")
            print(f"║ {Color.BLANCO}5. Ejecutar Planificador Round Robin{Color.CYAN}       ║")
            print(f"║ {Color.BLANCO}6. Salir{Color.CYAN}                                   ║")
            print(f"╚════════════════════════════════════════════╝{Color.RESET}")

            opcion = input(f"{Color.BLANCO}Seleccione una opción: {Color.RESET}")

            if opcion == "1": self.crear_proceso()
            elif opcion == "2": self.mostrar_procesos()
            elif opcion == "3": self.eliminar_proceso()
            elif opcion == "4": self.ejecutar_fcfs()
            elif opcion == "5": self.ejecutar_rr()
            elif opcion == "6":
                print(f"{Color.AMARILLO}Cerrando kernel y liberando memoria...{Color.RESET}"); break
            else:
                print(f"{Color.ROJO}Opción inválida.{Color.RESET}\n")

# Punto de entrada del programa
if __name__ == "__main__":
    sistema = SistemaOperativo()
    sistema.menu()
