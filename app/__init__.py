# app/__init__.py

from modelos.base import conectar_db
from managers.cliente_manager import ClienteManager
from managers.reserva_manager import ReservaManager
from managers.habitacion_manager import HabitacionManager

# Inicializamos la conexión y los gestores principales para que sean fácilmente accesibles
conn = conectar_db()
cliente_mgr = ClienteManager(conn)
reserva_mgr = ReservaManager(conn)
habitacion_mgr = HabitacionManager(conn)
