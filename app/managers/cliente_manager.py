import sqlite3
from tabulate import tabulate
from app.modelos.base import conectar_db
from app.modelos.cliente import Clientes

class Cliente_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def registrar_cliente(self, nombre, apellido, telefono, correo):
        try:
            while "@" not in correo:
                print("Error: el correo debe contener '@'.")
                correo = input("Ingrese nuevamente el correo: ")

            # Validar correo duplicado (solo clientes activos)
            self.cursor.execute("SELECT idCliente FROM Cliente WHERE Correo = ? AND activo = 1", (correo,))
            if self.cursor.fetchone():
                print("Ya existe un cliente activo con este correo.")
                return None

            # Insertar nuevo cliente
            self.cursor.execute("""
                INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo)
                VALUES (?, ?, ?, ?)
            """, (nombre, apellido, telefono, correo))
            self.conn.commit()
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error al registrar cliente: {e}")
            return None

    def listar_Clientes(self):
        try:
            # Solo clientes activos
            self.cursor.execute("SELECT * FROM Cliente WHERE activo = 1")
            filas = self.cursor.fetchall()
            return [Clientes(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar clientes: {e}")
            return []

    def mostrar_tabla_clientes(self, clientes):
        if clientes:
            data = [[c.idCliente, c.Nombre, c.Apellido, c.Telefono, c.Correo] for c in clientes]
            headers = ["ID", "Nombre", "Apellido", "Telefono", "Correo"]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("No hay clientes registrados.")

    def buscar_Clientes(self, idCliente):
        try:
            self.cursor.execute("SELECT * FROM Cliente WHERE idCliente = ? AND activo = 1", (idCliente,))
            client = self.cursor.fetchone()
            if client:
                return Clientes(*client)
            else:
                print("Cliente no encontrado o inactivo.")
                return None
        except sqlite3.Error as e:
            print(f"Error al buscar cliente: {e}")
            return None

    def eliminar_cliente(self, idCliente):
        try:
            # Marcamos al cliente como inactivo
            self.cursor.execute("UPDATE Cliente SET activo = 0 WHERE idCliente = ?", (idCliente,))
            
            # Cancelamos todas sus reservas activas
            self.cursor.execute("""
                UPDATE Reserva
                SET estadoReserva = 'cancelada'
                WHERE idCliente = ? AND estadoReserva != 'cancelada'
            """, (idCliente,))
            
            self.conn.commit()
            print("Cliente eliminado (lógicamente) y reservas canceladas con éxito.")
        except sqlite3.Error as e:
            print(f"Error al eliminar cliente: {e}")
    def exportar_clientes_csv(self):
        clientes = self.clientes.listar_Clientes()
        if clientes:
            datos = [(c.idCliente, c.Nombre, c.Apellido, c.Telefono, c.Correo) for c in clientes]
            encabezados = ["ID", "Nombre", "Apellido", "Telefono", "Correo"]
            self.exportar_csv(datos, encabezados, "clientes.csv")
        else:
            print("❌ No hay clientes para exportar")

