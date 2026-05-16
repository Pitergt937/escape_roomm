-- Active: 1778950130859@@127.0.0.1@3306
-- ============================================================
-- GESTOR ESCAPE ROOM -- Script de creación de la base de datos
-- ============================================================

CREATE TABLE IF NOT EXISTS salas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    dificultad TEXT NOT NULL,
    capacidad_max INTEGER NOT NULL CHECK(capacidad_max > 0),
    tiempo_limite_min INTEGER NOT NULL CHECK(tiempo_limite_min > 0),
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE,
    fecha_registro TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL,
    telefono TEXT
);

CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sala_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    num_jugadores INTEGER NOT NULL CHECK(num_jugadores > 0),
    estado TEXT NOT NULL CHECK(
        estado IN ('pendiente','confirmada','en curso','completada','cancelada')
    ),
    FOREIGN KEY (sala_id) REFERENCES salas(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

CREATE TABLE IF NOT EXISTS records (
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

CREATE TABLE IF NOT EXISTS penalizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    tiempo_suma_min INTEGER NOT NULL CHECK(tiempo_suma_min >= 0),
    FOREIGN KEY (record_id) REFERENCES records(id)
);