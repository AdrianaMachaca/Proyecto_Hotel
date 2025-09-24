class Reserva:
    def __init__(self, cliente, idReserva, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, cuenta):
        self.cliente = cliente
        self.idReserva = idReserva
        self.numHabit = numHabit
        self.idCliente = idCliente
        self.fechaEntrada = fechaEntrada
        self.fechaSalida = fechaSalida
        self.estadoReserva = estadoReserva
        self.servExtras = servExtras
        self.cuenta =  cuenta

    def mostrar_reserva(self):
        print(f"Reserva ID: {self.idReserva}")
        print(f"Habitación: {self.numHabit}")
        print(f"Cliente: {self.cliente.nombre} {self.cliente.apellido}")
        print(f"Entrada: {self.fechaEntrada}, Salida: {self.fechaSalida}")
        print(f"Estado: {self.estadoReserva}")
        print(f"Servicios extras: {self.servExtras}")   





