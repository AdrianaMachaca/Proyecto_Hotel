import sqlite3
from base import conectar_db
import os

def conectar_db(ruta="Base_Datos.db"):
    ruta_abs = os.path.abspath(ruta)
    print("Usando base de datos en:", ruta_abs)
    return sqlite3.connect(ruta_abs)

def mostrar_tabla(cursor, tabla):
    cursor.execute(f"SELECT * FROM {tabla}")
    filas = cursor.fetchall()
    if filas:
        print(f"\nDatos en la tabla {tabla}:")
        for fila in filas:
            print(fila)
    else:
        print(f"\nLa tabla {tabla} está vacía.")

def main():
    with conectar_db() as conn:
        cursor = conn.cursor()
        tablas = ["Cliente", "Habitacion", "Reserva"]
        for tabla in tablas:
            mostrar_tabla(cursor, tabla)
