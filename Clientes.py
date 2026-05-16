from database import conectar
from datetime import date


def crear_cliente():
    """Registra un nuevo cliente en la BD"""
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        nombre = input("Nombre del cliente: ").strip()
        telefono = input("Teléfono (opcional): ").strip()
        email = input("Email (opcional): ").strip()
        fecha_registro = str(date.today())  # Fecha de hoy automáticamente

        cursor.execute(
            """
            INSERT INTO clientes (nombre, telefono, email, fecha_registro)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, telefono or None, email or None, fecha_registro)
        )

        conexion.commit()
        print("Cliente registrado correctamente.")

    except Exception as e:
        print(f"Error al registrar cliente: {e}")
    finally:
        conexion.close()


def ver_clientes():
    """Muestra todos los clientes registrados"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexion.close()

    if not clientes:
        print("No hay clientes registrados.")
        return

    print("\n{:<5} {:<25} {:<15} {:<25} {}".format(
        "ID", "Nombre", "Teléfono", "Email", "Fecha registro"))
    print("-" * 80)
    for c in clientes:
        print("{:<5} {:<25} {:<15} {:<25} {}".format(
            c[0], c[1], c[2] or "-", c[3] or "-", c[4]))


def buscar_cliente():
    """Busca un cliente por nombre"""
    nombre = input("Nombre a buscar: ").strip()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM clientes WHERE nombre LIKE ?",
        (f"%{nombre}%",)
    )
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("No se encontraron clientes con ese nombre.")
        return

    print("\n{:<5} {:<25} {:<15} {:<25} {}".format(
        "ID", "Nombre", "Teléfono", "Email", "Fecha registro"))
    print("-" * 80)
    for c in resultados:
        print("{:<5} {:<25} {:<15} {:<25} {}".format(
            c[0], c[1], c[2] or "-", c[3] or "-", c[4]))


def modificar_cliente():
    """Modifica los datos de un cliente"""
    ver_clientes()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_cliente = int(input("\nID del cliente a modificar: "))

        cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
        if not cursor.fetchone():
            print("No existe ningún cliente con ese ID.")
            return

        print("¿Qué quieres modificar?")
        print("1. Nombre")
        print("2. Teléfono")
        print("3. Email")
        campo = input("Opción: ")

        if campo == "1":
            valor = input("Nuevo nombre: ").strip()
            cursor.execute("UPDATE clientes SET nombre = ? WHERE id = ?", (valor, id_cliente))
        elif campo == "2":
            valor = input("Nuevo teléfono: ").strip()
            cursor.execute("UPDATE clientes SET telefono = ? WHERE id = ?", (valor, id_cliente))
        elif campo == "3":
            valor = input("Nuevo email: ").strip()
            cursor.execute("UPDATE clientes SET email = ? WHERE id = ?", (valor, id_cliente))
        else:
            print("Opción inválida.")
            return

        conexion.commit()
        print("✔ Cliente modificado correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def eliminar_cliente():
    """Elimina un cliente si no tiene reservas activas"""
    ver_clientes()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_cliente = int(input("\nID del cliente a eliminar: "))

        cursor.execute(
            "SELECT COUNT(*) FROM reservas WHERE cliente_id = ? AND estado != 'cancelada'",
            (id_cliente,)
        )
        if cursor.fetchone()[0] > 0:
            print("No se puede eliminar: el cliente tiene reservas activas.")
            return

        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conexion.commit()
        print("✔ Cliente eliminado correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def menu_clientes():
    """Submenú de gestión de clientes"""
    while True:
        print("\n--- GESTIÓN DE CLIENTES ---")
        print("1. Registrar cliente")
        print("2. Ver clientes")
        print("3. Buscar cliente")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("6. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            ver_clientes()
        elif opcion == "3":
            buscar_cliente()
        elif opcion == "4":
            modificar_cliente()
        elif opcion == "5":
            eliminar_cliente()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")