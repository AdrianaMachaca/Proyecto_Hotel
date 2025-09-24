import sqlite3
from modelos.base import conectar_db
from managers.cliente_manager import Ciente_manager
from managers.habitacion_manager import Habitacion_manager
from managers.reserva_manager import Reserva_manager

def menu():
    conn = conectar_db() 
    cliente_mgr = Ciente_manager(conn)
    habitacion_mgr = Habitacion_manager(conn)
    reserva_mgr = Reserva_manager(conn)

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrar cliente")
        print("2. Crear reserva")
        print("3. Consultar reservas")
        print("4. Eliminar reserva")
        print("5. Mostrar disponibilidad")
        print("6. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Entrada inválida. Debe ser un número.")
            continue

        match opcion:
            case 1:
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                telefono = input("Teléfono: ")
                correo = input("Correo: ")
                idCliente = cliente_mgr.registrar_cliente(nombre, apellido, telefono, correo)

                crear = input("¿Desea crear una reserva para este cliente ahora? (s/n): ")
                if crear.lower() == "s":
                    numHabit = int(input("Número de habitación: "))
                    fechaEntrada = input("Fecha de entrada (YYYY-MM-DD): ")
                    fechaSalida = input("Fecha de salida (YYYY-MM-DD): ")
                    estado = input("Estado (Confirmada/Pendiente/Cancelada): ")
                    servicios = input("Servicios extras: ")
                    cuenta = float(input("Costo total: "))
                    reserva_mgr.crear_reserva(numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, cuenta)

            case 2:
                idCliente = int(input("ID del cliente: "))
                numHabit = int(input("Número de habitación: "))
                fechaEntrada = input("Fecha de entrada (YYYY-MM-DD): ")
                fechaSalida = input("Fecha de salida (YYYY-MM-DD): ")
                estado = input("Estado (Confirmada/Pendiente/Cancelada): ")
                servicios = input("Servicios extras: ")
                cuenta = float(input("Costo total: "))
                reserva_mgr.crear_reserva(numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, cuenta)

            case 3:
                idReserva = int(input("ID de la reserva a consultar: "))
                reserva_mgr.consultar_reservas(idReserva)

            case 4:
                idReserva = int(input("ID de la reserva a eliminar: "))
                reserva_mgr.eliminar_reserva(idReserva)

            case 5:
                numHabit = int(input("Número de habitación a consultar: "))
                mensaje = habitacion_mgr.Disponibilidad_habitaciones(numHabit)
                print(mensaje)
            case 6:
                print("Saliendo del sistema.")
                break
            case 7:
                print("Lista de clientes:")
                cliente_mgr.listar_Clientes()
            case _:
                print("Opción inválida.")


if __name__ == "__main__":
    menu()
