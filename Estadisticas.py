from database import conectar


def ver_estadisticas():
    """
    Muestra estadísticas generales por sala:
    total de reservas, tiempo medio de finalización y mejor récord.
    Consulta compleja con LEFT JOIN y funciones de agregación (COUNT, AVG, MIN).
    """
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT salas.nombre,
               COUNT(DISTINCT reservas.id)       AS total_reservas,
               COUNT(DISTINCT records.id)         AS sesiones_completadas,
               ROUND(AVG(records.tiempo_final_min), 1) AS tiempo_medio,
               MIN(records.tiempo_final_min)      AS mejor_tiempo
        FROM salas
        LEFT JOIN reservas ON salas.id = reservas.sala_id
        LEFT JOIN records  ON salas.id = records.sala_id
        GROUP BY salas.id
        ORDER BY salas.nombre
        """
    )
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("No hay datos suficientes para mostrar estadísticas.")
        return

    print("\n📊 ESTADÍSTICAS GENERALES")
    print("{:<20} {:<12} {:<12} {:<14} {}".format(
        "Sala", "Reservas", "Sesiones", "T.Medio", "Mejor récord"))
    print("-" * 68)
    for r in resultados:
        print("{:<20} {:<12} {:<12} {:<14} {}".format(
            r[0],
            r[1],
            r[2],
            f"{r[3]} min" if r[3] else "-",
            f"{r[4]} min" if r[4] else "-"
        ))