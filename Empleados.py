from database import conectar


def crear_empleado():
    """Registra un nuevo empleado en la BD."""
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        nombre = input("Nombre del empleado: ").strip()
        rol = input("Rol (empleado/admin): ").strip()
        telefono = input("Teléfono (opcional): ").strip()

        cursor.execute(
            """
            INSERT INTO empleados (nombre, rol, telefono)
            VALUES (?, ?, ?)
            """,
            (nombre, rol, telefono or None)
        )

        conexion.commit()
        print("✔ Empleado registrado correctamente.")

    except Exception as e:
        print(f"Error al registrar empleado: {e}")
    finally:
        conexion.close()


def ver_empleados():
    """Muestra todos los empleados registrados."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conexion.close()

    if not empleados:
        print("No hay empleados registrados.")
        return

    print("\n{:<5} {:<25} {:<12} {}".format("ID", "Nombre", "Rol", "Teléfono"))
    print("-" * 55)
    for e in empleados:
        print("{:<5} {:<25} {:<12} {}".format(e[0], e[1], e[2], e[3] or "-"))


def modificar_empleado():
    """Modifica los datos de un empleado."""
    ver_empleados()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_emp = int(input("\nID del empleado a modificar: "))

        cursor.execute("SELECT * FROM empleados WHERE id = ?", (id_emp,))
        if not cursor.fetchone():
            print("No existe ningún empleado con ese ID.")
            return

        print("¿Qué quieres modificar?")
        print("1. Nombre")
        print("2. Rol")
        print("3. Teléfono")
        campo = input("Opción: ")

        if campo == "1":
            valor = input("Nuevo nombre: ").strip()
            cursor.execute("UPDATE empleados SET nombre = ? WHERE id = ?", (valor, id_emp))
        elif campo == "2":
            valor = input("Nuevo rol: ").strip()
            cursor.execute("UPDATE empleados SET rol = ? WHERE id = ?", (valor, id_emp))
        elif campo == "3":
            valor = input("Nuevo teléfono: ").strip()
            cursor.execute("UPDATE empleados SET telefono = ? WHERE id = ?", (valor, id_emp))
        else:
            print("Opción inválida.")
            return

        conexion.commit()
        print("✔ Empleado modificado correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def eliminar_empleado():
    """Elimina un empleado si no tiene reservas asignadas."""
    ver_empleados()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_emp = int(input("\nID del empleado a eliminar: "))

        cursor.execute(
            "SELECT COUNT(*) FROM reservas WHERE empleado_id = ? AND estado != 'cancelada'",
            (id_emp,)
        )
        if cursor.fetchone()[0] > 0:
            print("No se puede eliminar: el empleado tiene reservas activas asignadas.")
            return

        cursor.execute("DELETE FROM empleados WHERE id = ?", (id_emp,))
        conexion.commit()
        print("✔ Empleado eliminado correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def menu_empleados():
    """Submenú de gestión de empleados."""
    while True:
        print("\n--- GESTIÓN DE EMPLEADOS ---")
        print("1. Registrar empleado")
        print("2. Ver empleados")
        print("3. Modificar empleado")
        print("4. Eliminar empleado")
        print("5. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            crear_empleado()
        elif opcion == "2":
            ver_empleados()
        elif opcion == "3":
            modificar_empleado()
        elif opcion == "4":
            eliminar_empleado()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")