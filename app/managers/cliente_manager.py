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
            # Validación básica del correo
            while "@" not in correo:
                print("Error: el correo electronico debe contener '@'.")
                correo = input("Ingrese nuevamente el correo: ")

            # ---- VALIDACION: correo duplicado ----
            self.cursor.execute("SELECT idCliente FROM Cliente WHERE Correo = ?", (correo,))
            if self.cursor.fetchone():
                print("Ya existe un cliente con este correo.")
                return None
            # --------------------------------------

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
            self.cursor.execute("SELECT * FROM Cliente")
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
            self.cursor.execute("""SELECT * FROM Cliente WHERE idCliente = ?""", (idCliente,))
            client = self.cursor.fetchone()
            if client:
                return Clientes(*client)
            else:
                print("Cliente no encontrado.")
                return None
        except sqlite3.Error as e:
            print(f"Error al buscar cliente: {e}")
            return None
