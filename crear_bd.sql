PRAGMA foreign_keys = ON;
        estado IN ('pendiente','confirmada','en curso','completada','cancelada')
    ),

    FOREIGN KEY (sala_id) REFERENCES salas(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER NOT NULL,
    sala_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    tiempo_real_min INTEGER NOT NULL,
    tiempo_final_min INTEGER,
    fecha TEXT NOT NULL,

    FOREIGN KEY (reserva_id) REFERENCES reservas(id),
    FOREIGN KEY (sala_id) REFERENCES salas(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE penalizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    tiempo_suma_min INTEGER NOT NULL CHECK(tiempo_suma_min >= 0),

    FOREIGN KEY (record_id) REFERENCES records(id)
);