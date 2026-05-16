import sqlite3


def conectar():
    """Abre y devuelve una conexión a la base de datos con claves foráneas activadas."""
    conexion = sqlite3.connect("escape_room.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def init_db():
    """Crea todas las tablas leyendo el script SQL si no existen todavía."""
    conexion = conectar()
    with open("crear_bd.sql", "r", encoding="utf-8") as f:
        conexion.executescript(f.read())
    conexion.close()