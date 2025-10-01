from app.modelos.base import conectar_db
from app.managers.cliente_manager import Cliente_manager
from app.managers.reserva_manager import Reserva_manager
from app.managers.habitacion_manager import Habitacion_manager

conn = conectar_db()
cliente_mgr = Cliente_manager(conn)
reserva_mgr = Reserva_manager(conn)
habitacion_mgr = Habitacion_manager(conn)
