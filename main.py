import ipaddress
from rich.table import Table
from rich.console import Console


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class RouterHash:
    def __init__(self, tam_usuario=7):
        self.tamaño = tam_usuario
        self.tabla = [None] * tam_usuario

    def ip_a_int(self, ip):
        octetos_transformados = list(map(int, ip.split(".")))
        return (octetos_transformados[0] << 24) + (octetos_transformados[1] << 16) + (octetos_transformados[2] << 8) + \
            octetos_transformados[3]

    def _hash(self, ip):
        value = self.ip_a_int(ip)
        return value % self.tamaño

    def agregar_ruta(self, ip, interfaz):
        index = self._hash(ip)
        original = index
        while self.tabla[index] is not None:
            if self.tabla[index][0] == ip:
                self.tabla[index] = (ip, interfaz)
                return
            index = (index + 1) % self.tamaño
            if index == original:
                raise Exception("Tabla llena")
        self.tabla[index] = (ip, interfaz)

    def encontrar_ruta(self, ip):
        index = self._hash(ip)
        original = index
        while self.tabla[index] is not None:
            if self.tabla[index][0] == ip:
                return self.tabla[index][1], index
            index = (index + 1) % self.tamaño
            if index == original:
                break
        return None, None

    def mostrar_tabla(self):
        print("\nTabla Hash:")
        for i, entry in enumerate(self.tabla):
            if entry:
                print(f"Índice {i}: {entry[0]} → {entry[1]}")
            else:
                print(f"Índice {i}: [Vacio]")

    def mostrar_tabla2(self):
        console = Console()
        table = Table(title="Tabla Hash")
        table.add_column("Índice", justify="center", style="cyan", no_wrap=True)
        table.add_column("IP", style="green")
        table.add_column("Interfaz", style="magenta")

        for i, entry in enumerate(self.tabla):
            if entry:
                table.add_row(str(i), entry[0], entry[1])
            else:
                table.add_row(str(i), "[italic red]Vacío[/]", "-")

        console.print(table)


def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def menu():
    router = RouterHash(7)

    while True:
        print("\n--- MENÚ ROUTER HASH ---")
        print("1. Agregar ruta")
        print("2. Buscar ruta")
        print("3. Eliminar ruta")
        print("4. Mostrar tabla")
        print("5. Simular paquete")
        print("6. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print(f"{RED}¡ERROR! Ingresa un número válido.{RESET}")
            continue

        match opcion:
            case 1:
                print("\n--- Agregar Ruta ---")
                ip = input("Ingrese IP destino: ")
                if not validar_ip(ip):
                    print(f"{RED}¡ERROR! IP no válida.{RESET}")
                    continue
                iface = input("Ingrese interfaz (ej. eth0): ")
                router.agregar_ruta(ip, iface)
                print(f"{GREEN}Ruta agregada.{RESET}")

            case 2:
                print("\n--- Buscar Ruta ---")
                ip = input("Ingrese IP a buscar: ")
                if not validar_ip(ip):
                    print(f"{RED}¡ERROR! IP no válida.{RESET}")
                    continue
                iface, idx = router.encontrar_ruta(ip)
                if iface:
                    print(f"{GREEN}IP {ip} encontrada en índice {idx} → {iface}{RESET}")
                else:
                    print(f"{RED}Ruta no encontrada.{RESET}")

            case 3:
                print("\n--- Eliminar Ruta ---")
                ip = input("Ingrese IP a eliminar: ")
                if not validar_ip(ip):
                    print(f"{RED}¡ERROR! IP no válida.{RESET}")
                    continue
                iface, idx = router.encontrar_ruta(ip)
                if iface:
                    router.tabla[idx] = None
                    print(f"{GREEN}Ruta {ip} eliminada.{RESET}")
                else:
                    print(f"{RED}Ruta no encontrada.{RESET}")

            case 4:
                print("\n--- Mostrar Tabla ---")
                router.mostrar_tabla2()

            case 5:
                print("\n--- Simular Paquete ---")
                ip = input("Ingrese IP destino del paquete: ")
                if not validar_ip(ip):
                    print(f"{RED}¡ERROR! IP no válida.{RESET}")
                    continue
                iface, idx = router.encontrar_ruta(ip)
                if iface:
                    print(f"{GREEN}Paquete destino {ip} → salir por {iface}{RESET}")
                else:
                    print(f"{RED}Paquete destino {ip} → DROP (no hay ruta){RESET}")

            case 6:
                print(f"{BLUE}Saliendo del simulador...{RESET}")
                break

            case _:
                print(f"{YELLOW}¡ERROR! Opción no válida.{RESET}")


menu()