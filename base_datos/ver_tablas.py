from tabulate import tabulate
import sqlite3

conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Cliente")
filas = cursor.fetchall()

# Obtener nombres de columnas
columnas = [descripcion[0] for descripcion in cursor.description]

# Mostrar como tabla
print(tabulate(filas, headers=columnas, tablefmt="grid"))

conn.close()
