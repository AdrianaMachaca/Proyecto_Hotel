import sqlite3
from modelos.base import conectar_db
from modelos.habitacion import Habitacion

class Habitacion_manager:
    def __init__(self,conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def Disponibilidad_habitaciones(self, numHabitacion):
        self.cursor.execute("SELECT * FROM Reserva WHERE numHabit = ?", (numHabitacion,))
        reserva = self.cursor.fetchone()
        if reserva:
            return f"Habitación {numHabitacion} NO está disponible"
        else:
            return f"Habitación {numHabitacion} está disponible"

    def crear_habitacion(self,numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones):
        self.cursor.execute("""SELECT * FROM Habitacion WHERE numHabitacion = ?""",(numHabitacion,))
        habita = self.cursor.fetchone()
        if habita:
            print("La habitacion ya existe")
            fila = Habitacion(*habita)
        else:
            self.cursor.execute("""
                INSERT INTO Habitacion(numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
                VALUES (?,?,?,?,?,?,?)
            """,(numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones))            
            self.conn.commit()
            print(f"Habitacion creada con éxito")
            return Habitacion(numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
