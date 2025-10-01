import sqlite3
from modelos.base import conectar_db
from modelos.cliente import Clientes

class Cliente_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def registrar_cliente(self, nombre, apellido, telefono, correo):
        try:
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
