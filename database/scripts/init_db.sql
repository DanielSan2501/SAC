-- SQLite

-- Base de Datos SAC - Sistema de Atencion Canina

---------------------------------
-- TABLA USUARIO
---------------------------------

CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoDocumento TEXT NOT NULL,
    numeroDocumento TEXT UNIQUE NOT NULL,
    nombreCompleto TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    telefono TEXT,
    rol TEXT NOT NULL,
    fechaRegistro DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    estado INTEGER NOT NULL CHECK (estado IN (0, 1))
);

-- Insertar Usuario Cliente de Prueba 
INSERT INTO Usuario (tipoDocumento, numeroDocumento, nombreCompleto, correo, contraseña, telefono, rol, estado)
VALUES ('CC', '1010014049', 'Cliente SAC', 'cliente@sac.com', '1234', '3229492459', 'cliente', 1);

-- Insertar Usuario Clinica de Prueba
INSERT INTO Usuario (tipoDocumento, numeroDocumento, nombreCompleto, correo, contraseña, telefono, rol, estado)
VALUES ('CC', '39762112', 'Clinica SAC', 'clinica@sac.com', '1234', '3124744378', 'clinica', 1);

---------------------------------
-- TABLA MASCOTA
---------------------------------

CREATE TABLE IF NOT EXISTS Mascota (
    idMascota INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    raza TEXT,
    sexo TEXT NOT NULL,
    edad INTEGER,
    peso REAL NOT NULL,
    fechaNacimiento DATE,
    estado INTEGER NOT NULL CHECK (estado IN (0, 1)),
    idUsuario INTEGER NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

---------------------------------
-- TABLA CLINICA
---------------------------------

CREATE TABLE IF NOT EXISTS Clinica (
    idClinica INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL,
    estado INTEGER NOT NULL CHECK (estado IN (0,1)) DEFAULT 0,
    idUsuario INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Simulacion cambio de estado de clinica a verificada
UPDATE Clinica SET estado = 1 WHERE idClinica = 1;

----------------------------------
-- TABLA SERVICIO
----------------------------------

CREATE TABLE IF NOT EXISTS Servicio (
    idServicio INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoServicio TEXT NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    duracion INTEGER NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1,
    idClinica INTEGER NOT NULL,

    FOREIGN KEY (idClinica) REFERENCES Clinica(idClinica)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

----------------------------------
-- TABLA CITA
----------------------------------

CREATE TABLE IF NOT EXISTS Cita (
    idCita INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,  -- aquí va fecha + hora
    observaciones TEXT,
    estado TEXT NOT NULL,
    idUsuario INTEGER NOT NULL,
    idMascota INTEGER NOT NULL,
    idClinica INTEGER NOT NULL,
    idServicio INTEGER NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (idMascota) REFERENCES Mascota(idMascota)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (idClinica) REFERENCES Clinica(idClinica)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (idServicio) REFERENCES Servicio(idServicio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


