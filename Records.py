from database import conectar


# Penalizaciones predefinidas según el enunciado
PENALIZACIONES = {
    "1": ("Uso del móvil",   5),
    "2": ("Romper elemento", 10),
    "3": ("Pista extra",     3),
    "4": ("Saltarse norma",  5),
}


def registrar_resultado():
    """
    Registra el resultado de una sesión completada.
    Usa una transacción: si algo falla → rollback completo.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Mostramos las reservas en curso para que sea fácil elegir
        cursor.execute(
            """
            SELECT reservas.id, salas.nombre, clientes.nombre, reservas.fecha
            FROM reservas
            JOIN salas    ON reservas.sala_id    = salas.id
            JOIN clientes ON reservas.cliente_id = clientes.id
            WHERE reservas.estado IN ('confirmada', 'en curso')
            """
        )
        reservas = cursor.fetchall()

        if not reservas:
            print("No hay reservas confirmadas o en curso.")
            return

        print("\nReservas disponibles para registrar resultado:")
        print("{:<5} {:<18} {:<20} {}".format("ID", "Sala", "Cliente", "Fecha"))
        print("-" * 55)
        for r in reservas:
            print("{:<5} {:<18} {:<20} {}".format(r[0], r[1], r[2], r[3]))

        reserva_id = int(input("\nID de la reserva: "))

        # Recuperamos sala_id y cliente_id de esa reserva
        cursor.execute(
            "SELECT sala_id, cliente_id FROM reservas WHERE id = ?",
            (reserva_id,)
        )
        fila = cursor.fetchone()
        if not fila:
            print("No existe esa reserva.")
            return

        sala_id, cliente_id = fila

        while True:
            try:
                tiempo_real = int(input("Tiempo real empleado (minutos): "))
                if tiempo_real > 0:
                    break
                print("Debe ser mayor que 0.")
            except ValueError:
                print("Introduce un número válido.")

        fecha = input("Fecha de la sesión (YYYY-MM-DD): ").strip()

        # INICIO DE TRANSACCIÓN 
        conexion.execute("BEGIN")

        # Paso 1: insertar el record
        cursor.execute(
            """
            INSERT INTO records
            (reserva_id, sala_id, cliente_id, tiempo_real_min, fecha)
            VALUES (?, ?, ?, ?, ?)
            """,
            (reserva_id, sala_id, cliente_id, tiempo_real, fecha)
        )
        record_id = cursor.lastrowid

        # Paso 2: añadir penalizaciones
        total_penalizacion = 0

        while True:
            print("\n¿Añadir penalización?")
            print("1. Uso del móvil     (+5 min)")
            print("2. Romper elemento   (+10 min)")
            print("3. Pista extra       (+3 min)")
            print("4. Saltarse norma    (+5 min)")
            print("5. No añadir más")

            opcion = input("Opción: ")

            if opcion == "5":
                break

            if opcion not in PENALIZACIONES:
                print("Opción inválida.")
                continue

            tipo, tiempo_pen = PENALIZACIONES[opcion]
            descripcion = input("Descripción adicional (opcional): ").strip()
            total_penalizacion += tiempo_pen

            cursor.execute(
                """
                INSERT INTO penalizaciones
                (record_id, tipo, descripcion, tiempo_suma_min)
                VALUES (?, ?, ?, ?)
                """,
                (record_id, tipo, descripcion or None, tiempo_pen)
            )
            print(f"  Penalización '{tipo}' añadida (+{tiempo_pen} min).")

        # Paso 3: calcular tiempo final y actualizar el record
        tiempo_final = tiempo_real + total_penalizacion
        cursor.execute(
            "UPDATE records SET tiempo_final_min = ? WHERE id = ?",
            (tiempo_final, record_id)
        )

        # Paso 4: marcar la reserva como completada
        cursor.execute(
            "UPDATE reservas SET estado = 'completada' WHERE id = ?",
            (reserva_id,)
        )

        # COMMIT si fue bien
        conexion.commit()
        print(f"\n✔ Resultado registrado. Tiempo final: {tiempo_final} min "
              f"({tiempo_real} real + {total_penalizacion} penalizaciones).")

    except ValueError:
        conexion.rollback()
        print("Error: dato inválido. Se ha cancelado la operación.")
    except Exception as e:
        conexion.rollback()
        print(f"Error en la transacción (rollback aplicado): {e}")
    finally:
        conexion.close()


def ver_ranking():
    """
    Muestra el ranking de récords de una sala ordenado por tiempo_final_min.
    Consulta compleja con JOIN entre 4 tablas y SUM como agregación.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    # Primero mostramos las salas disponibles
    cursor.execute("SELECT id, nombre FROM salas")
    salas = cursor.fetchall()

    if not salas:
        print("No hay salas registradas.")
        conexion.close()
        return

    print("\nSalas disponibles:")
    for s in salas:
        print(f"  {s[0]}. {s[1]}")

    try:
        sala_id = int(input("ID de la sala para ver el ranking: "))
    except ValueError:
        print("Introduce un número válido.")
        conexion.close()
        return

    cursor.execute(
        """
        SELECT clientes.nombre,
               records.tiempo_real_min,
               COALESCE(SUM(penalizaciones.tiempo_suma_min), 0) AS total_penalizacion,
               records.tiempo_final_min,
               records.fecha
        FROM records
        JOIN salas    ON records.sala_id    = salas.id
        JOIN clientes ON records.cliente_id = clientes.id
        LEFT JOIN penalizaciones ON penalizaciones.record_id = records.id
        WHERE salas.id = ?
        GROUP BY records.id
        ORDER BY records.tiempo_final_min ASC
        """,
        (sala_id,)
    )
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("No hay récords para esta sala todavía.")
        return

    # Obtenemos el nombre de la sala para el título
    print(f"\n🏆 RANKING — {salas[[s[0] for s in salas].index(sala_id)][1]}")
    print("{:<5} {:<22} {:<12} {:<14} {:<14} {}".format(
        "Pos", "Cliente", "T.Real", "Penalización", "T.Final", "Fecha"))
    print("-" * 75)
    for pos, r in enumerate(resultados, start=1):
        print("{:<5} {:<22} {:<12} {:<14} {:<14} {}".format(
            pos, r[0], f"{r[1]} min", f"+{r[2]} min", f"{r[3]} min", r[4]))