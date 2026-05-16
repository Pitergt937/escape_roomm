from database import init_db
from menus import menu_principal


if __name__ == "__main__":
    # Crea la base de datos y las tablas si no existen todavía
    init_db()
    # Lanza el menú principal
    menu_principal()