import sqlite3
from modelos.base import conectar_db
from modelos.cliente import Clientes

class Ciente_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def registrar_cliente(self, nombre, apellido, telefono, correo):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo)
            VALUES (?, ?, ?, ?)
        """, (nombre, apellido, telefono, correo))
        self.conn.commit()
        return cursor.lastrowid
    
    def listar_Clientes(self):
        self.cursor.execute("SELECT * FROM Cliente")
        filas = self.cursor.fetchall()
        return [Clientes(*fila) for fila in filas]


    def buscar_Clientes(self,idCliente):
        self.cursor.execute("""SELECT * FROM Cliente WHERE idCliente = ?""",(idCliente))
        client = self.cursor.fetchone()
        if client:
         fila = Clientes(*client)
        return None

