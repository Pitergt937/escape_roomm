from database import conectar


def crear_sala():
    """Pide los datos de una sala nueva y la inserta en la BD"""
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        nombre = input("Nombre de la sala: ").strip()
        dificultad = input("Dificultad (fácil/medio/difícil): ").strip()

        # Comprobamos que capacidad y tiempo sean números positivos
        while True:
            try:
                capacidad = int(input("Capacidad máxima de jugadores: "))
                if capacidad > 0:
                    break
                print("Debe ser un número mayor que 0.")
            except ValueError:
                print("Introduce un número válido.")

        while True:
            try:
                tiempo = int(input("Tiempo límite en minutos: "))
                if tiempo > 0:
                    break
                print("Debe ser un número mayor que 0.")
            except ValueError:
                print("Introduce un número válido.")

        descripcion = input("Descripción (opcional): ").strip()

        cursor.execute(
            """
            INSERT INTO salas (nombre, dificultad, capacidad_max, tiempo_limite_min, descripcion)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, dificultad, capacidad, tiempo, descripcion)
        )

        conexion.commit()
        print("✔ Sala creada correctamente.")

    except Exception as e:
        print(f"Error al crear la sala: {e}")

    finally:
        conexion.close()


def ver_salas():
    """Muestra todas las salas registradas"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM salas")
    salas = cursor.fetchall()
    conexion.close()

    if not salas:
        print("No hay salas registradas.")
        return

    print("\n{:<5} {:<20} {:<10} {:<12} {:<12} {}".format(
        "ID", "Nombre", "Dificultad", "Capacidad", "T.Límite", "Descripción"))
    print("-" * 75)
    for sala in salas:
        print("{:<5} {:<20} {:<10} {:<12} {:<12} {}".format(
            sala[0], sala[1], sala[2], sala[3], sala[4], sala[5] or ""))


def modificar_sala():
    """Modifica los datos de una sala existente"""
    ver_salas()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_sala = int(input("\nID de la sala a modificar: "))

        # Comprobamos que la sala existe
        cursor.execute("SELECT * FROM salas WHERE id = ?", (id_sala,))
        if not cursor.fetchone():
            print("No existe ninguna sala con ese ID.")
            return

        print("¿Qué quieres modificar?")
        print("1. Nombre")
        print("2. Dificultad")
        print("3. Capacidad máxima")
        print("4. Tiempo límite")
        print("5. Descripción")
        campo = input("Opción: ")

        if campo == "1":
            valor = input("Nuevo nombre: ").strip()
            cursor.execute("UPDATE salas SET nombre = ? WHERE id = ?", (valor, id_sala))
        elif campo == "2":
            valor = input("Nueva dificultad: ").strip()
            cursor.execute("UPDATE salas SET dificultad = ? WHERE id = ?", (valor, id_sala))
        elif campo == "3":
            valor = int(input("Nueva capacidad: "))
            cursor.execute("UPDATE salas SET capacidad_max = ? WHERE id = ?", (valor, id_sala))
        elif campo == "4":
            valor = int(input("Nuevo tiempo límite (min): "))
            cursor.execute("UPDATE salas SET tiempo_limite_min = ? WHERE id = ?", (valor, id_sala))
        elif campo == "5":
            valor = input("Nueva descripción: ").strip()
            cursor.execute("UPDATE salas SET descripcion = ? WHERE id = ?", (valor, id_sala))
        else:
            print("Opción inválida.")
            return

        conexion.commit()
        print("✔ Sala modificada correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def eliminar_sala():
    """Elimina una sala"""
    ver_salas()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_sala = int(input("\nID de la sala a eliminar: "))

        # Comprobamos reservas activas antes de borrar
        cursor.execute(
            "SELECT COUNT(*) FROM reservas WHERE sala_id = ? AND estado != 'cancelada'",
            (id_sala,)
        )
        if cursor.fetchone()[0] > 0:
            print("No se puede eliminar: la sala tiene reservas activas.")
            return

        cursor.execute("DELETE FROM salas WHERE id = ?", (id_sala,))
        conexion.commit()
        print("✔ Sala eliminada correctamente.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error al eliminar la sala: {e}")
    finally:
        conexion.close()


def menu_salas():
    """Submenú de gestión de salas."""
    while True:
        print("\n--- GESTIÓN DE SALAS ---")
        print("1. Crear sala")
        print("2. Ver salas")
        print("3. Modificar sala")
        print("4. Eliminar sala")
        print("5. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            crear_sala()
        elif opcion == "2":
            ver_salas()
        elif opcion == "3":
            modificar_sala()
        elif opcion == "4":
            eliminar_sala()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")