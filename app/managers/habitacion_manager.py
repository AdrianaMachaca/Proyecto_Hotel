import sqlite3
from app.modelos.base import conectar_db
from app.modelos.habitacion import Habitacion

class Habitacion_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def disponibilidad_habitaciones(self, numHabitacion):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE numHabit = ?", (numHabitacion,))
            reserva = self.cursor.fetchone()
            if reserva:
                return f"Habitación {numHabitacion} NO está disponible"
            else:
                return f"Habitación {numHabitacion} está disponible"
        except sqlite3.Error as e:
            print(f"Error al comprobar disponibilidad: {e}")
            return "Error al verificar disponibilidad."

    def crear_habitacion(self, numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones):
        try:
            # Comprobamos si la habitación ya existe
            self.cursor.execute("SELECT * FROM Habitacion WHERE numHabitacion = ?", (numHabitacion,))
            habita = self.cursor.fetchone()

            if habita:
                print("La habitación ya existe")
                return Habitacion(*habita)  # Retornamos el objeto ya existente
            else:
                self.cursor.execute("""
                    INSERT INTO Habitacion (Num_Habitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones))
                self.conn.commit()
                print(f"Habitación creada con éxito")
                return Habitacion(numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
        except sqlite3.Error as e:
            print(f"Error al crear habitación: {e}")
            return None
