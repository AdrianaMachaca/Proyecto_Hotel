import sqlite3
from app.modelos.base import conectar_db

class Clientes:
    def __init__(self, idCliente, Nombre, Apellido, Telefono, Correo, Activo = 1):
        self.idCliente = idCliente
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Telefono = Telefono
        self.Correo = Correo
        self.Activo = Activo

    def guardar(self):
        conexion = conectar_db()  # Asume que ya tienes un método para conectar
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo)
            VALUES (?, ?, ?, ?)
        """, (self.Nombre, self.Apellido, self.Telefono, self.Correo))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_todos(cls):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente")
        filas = cursor.fetchall()
        conexion.close()
        return [cls(*fila) for fila in filas]
