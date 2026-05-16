from database import conectar
from salas import ver_salas
from clientes import ver_clientes
from empleados import ver_empleados


def crear_reserva():
    """Crea una nueva reserva comprobando que la sala no esté ocupada."""
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        ver_salas()
        sala_id = int(input("\nID de la sala: "))

        ver_clientes()
        cliente_id = int(input("\nID del cliente: "))

        ver_empleados()
        empleado_id = int(input("\nID del empleado asignado: "))

        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        hora = input("Hora (HH:MM): ").strip()

        while True:
            try:
                num_jugadores = int(input("Número de jugadores: "))
                if num_jugadores > 0:
                    break
                print("Debe ser mayor que 0.")
            except ValueError:
                print("Introduce un número válido.")

        # Comprobamos que la sala no esté ya reservada en esa franja
        cursor.execute(
            """
            SELECT * FROM reservas
            WHERE sala_id = ? AND fecha = ? AND hora = ?
            AND estado != 'cancelada'
            """,
            (sala_id, fecha, hora)
        )
        if cursor.fetchone():
            print("⚠ La sala ya está reservada en esa franja horaria.")
            return

        cursor.execute(
            """
            INSERT INTO reservas
            (sala_id, cliente_id, empleado_id, fecha, hora, num_jugadores, estado)
            VALUES (?, ?, ?, ?, ?, ?, 'pendiente')
            """,
            (sala_id, cliente_id, empleado_id, fecha, hora, num_jugadores)
        )

        conexion.commit()
        print("✔ Reserva creada correctamente.")

    except ValueError:
        print("Introduce un valor válido.")
    except Exception as e:
        print(f"Error al crear la reserva: {e}")
    finally:
        conexion.close()


def ver_reservas():
    """Muestra todas las reservas con información de sala y cliente."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT reservas.id, salas.nombre, clientes.nombre,
               reservas.fecha, reservas.hora,
               reservas.num_jugadores, reservas.estado
        FROM reservas
        JOIN salas    ON reservas.sala_id    = salas.id
        JOIN clientes ON reservas.cliente_id = clientes.id
        ORDER BY reservas.fecha, reservas.hora
        """
    )
    reservas = cursor.fetchall()
    conexion.close()

    if not reservas:
        print("No hay reservas registradas.")
        return

    print("\n{:<5} {:<18} {:<20} {:<12} {:<8} {:<10} {}".format(
        "ID", "Sala", "Cliente", "Fecha", "Hora", "Jugadores", "Estado"))
    print("-" * 85)
    for r in reservas:
        print("{:<5} {:<18} {:<20} {:<12} {:<8} {:<10} {}".format(
            r[0], r[1], r[2], r[3], r[4], r[5], r[6]))


def ver_reservas_por_fecha():
    """Filtra reservas por una fecha concreta."""
    fecha = input("Fecha a consultar (YYYY-MM-DD): ").strip()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT reservas.id, salas.nombre, clientes.nombre,
               reservas.hora, reservas.num_jugadores, reservas.estado
        FROM reservas
        JOIN salas    ON reservas.sala_id    = salas.id
        JOIN clientes ON reservas.cliente_id = clientes.id
        WHERE reservas.fecha = ?
        ORDER BY reservas.hora
        """,
        (fecha,)
    )
    reservas = cursor.fetchall()
    conexion.close()

    if not reservas:
        print(f"No hay reservas para el {fecha}.")
        return

    print(f"\nReservas para el {fecha}:")
    print("{:<5} {:<18} {:<20} {:<8} {:<10} {}".format(
        "ID", "Sala", "Cliente", "Hora", "Jugadores", "Estado"))
    print("-" * 70)
    for r in reservas:
        print("{:<5} {:<18} {:<20} {:<8} {:<10} {}".format(
            r[0], r[1], r[2], r[3], r[4], r[5]))


def cambiar_estado_reserva():
    """Cambia el estado de una reserva (pendiente → en curso → completada / cancelada)."""
    ver_reservas()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_reserva = int(input("\nID de la reserva: "))

        cursor.execute("SELECT estado FROM reservas WHERE id = ?", (id_reserva,))
        fila = cursor.fetchone()
        if not fila:
            print("No existe ninguna reserva con ese ID.")
            return

        print(f"Estado actual: {fila[0]}")
        print("Nuevo estado:")
        print("1. pendiente")
        print("2. confirmada")
        print("3. en curso")
        print("4. completada")
        print("5. cancelada")
        opcion = input("Opción: ")

        estados = {
            "1": "pendiente",
            "2": "confirmada",
            "3": "en curso",
            "4": "completada",
            "5": "cancelada"
        }

        if opcion not in estados:
            print("Opción inválida.")
            return

        cursor.execute(
            "UPDATE reservas SET estado = ? WHERE id = ?",
            (estados[opcion], id_reserva)
        )
        conexion.commit()
        print(f"✔ Estado cambiado a '{estados[opcion]}'.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def cancelar_reserva():
    """Cancela una reserva cambiando su estado a 'cancelada'."""
    ver_reservas()
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        id_reserva = int(input("\nID de la reserva a cancelar: "))

        cursor.execute(
            "UPDATE reservas SET estado = 'cancelada' WHERE id = ?",
            (id_reserva,)
        )
        if cursor.rowcount == 0:
            print("No existe ninguna reserva con ese ID.")
        else:
            conexion.commit()
            print("✔ Reserva cancelada.")

    except ValueError:
        print("Introduce un número válido.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()


def menu_reservas():
    """Submenú de gestión de reservas."""
    while True:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Crear reserva")
        print("2. Ver todas las reservas")
        print("3. Ver reservas por fecha")
        print("4. Cambiar estado de reserva")
        print("5. Cancelar reserva")
        print("6. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            crear_reserva()
        elif opcion == "2":
            ver_reservas()
        elif opcion == "3":
            ver_reservas_por_fecha()
        elif opcion == "4":
            cambiar_estado_reserva()
        elif opcion == "5":
            cancelar_reserva()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")