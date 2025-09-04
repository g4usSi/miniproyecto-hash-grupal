class RouterHash:
    def __init__(self, tam_usuario = 7):
        self.tamaño = tam_usuario
        self.tabla = [None] * tam_usuario

    def ip_a_int(self, ip):
        octetos_transformados = list(map(int, ip.split(".")))
        return (octetos_transformados[0] << 24) + (octetos_transformados[1] << 16) + (octetos_transformados[2] << 8) + octetos_transformados[3]

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


#SIMULACION EN CONSOLA
router = RouterHash()

# Rutas iniciales
router.agregar_ruta("192.168.1.1", "eth0")
router.agregar_ruta("10.0.0.2", "eth1")
router.agregar_ruta("172.16.5.10", "eth2")
router.agregar_ruta("8.8.8.8", "eth3")
router.agregar_ruta("192.168.1.99", "eth0")

# Mostrar tabla
router.mostrar_tabla()

# Simulación de busqueda
ip = "192.168.1.1"
iface, idx = router.encontrar_ruta(ip)
if iface:
    print(f"\nPaquete destino {ip}: encontrado en indice {idx} → salida {iface}")
else:
    print(f"\nPaquete destino {ip}: no encontrado")
