import sqlite3
from app.modelos.base import conectar_db

class Habitacion:
    def __init__(self, numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones):
        self.numHabitacion = numHabitacion
        self.Tipo = Tipo
        self.Estado = Estado
        self.Precio = Precio
        self.Capacidad = Capacidad
        self.Servicios = Servicios
        self.Observaciones = Observaciones
    
    
    def guardar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Habitacion (Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.Tipo, self.Estado, self.Precio, self.Capacidad, self.Servicios, self.Observaciones))
        conexion.commit()
        conexion.close()