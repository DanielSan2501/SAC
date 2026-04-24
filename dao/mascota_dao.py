import sqlite3
from models.mascota_model import Mascota

Datos = "database/sac.db"

class MascotaDAO:

    def validar_mascota_registrada(self, nombre, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT 1 FROM Mascota WHERE nombre = ? AND idUsuario = ? LIMIT 1"
        cursor.execute(query, (nombre, id_usuario))

        resultado = cursor.fetchone()

        conn.close()

        return resultado is not None

    def registrar_mascota(self, mascota):

        conn = sqlite3.connect(Datos)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        query = """
            INSERT INTO Mascota (
                nombre, especie, raza, sexo, edad, peso, fechaNacimiento, estado, idUsuario
            ) Values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            mascota.nombre,
            mascota.especie,
            mascota.raza,
            mascota.sexo,
            mascota.edad,
            mascota.peso,
            mascota.fecha_nacimiento,
            mascota.estado,
            mascota.id_usuario
        ))

        conn.commit()
        conn.close()

    def obtener_mascotas_por_usuario(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
        SELECT idMascota, nombre, especie, raza, sexo, edad, peso, fechaNacimiento, estado, idUsuario
        FROM Mascota 
        WHERE idUsuario = ?
        """
        cursor.execute(query, (id_usuario,))

        filas = cursor.fetchall()
        mascotas = []

        for fila in filas:
            mascota = Mascota(
                id_mascota=fila[0],
                nombre=fila[1],
                especie=fila[2],
                raza=fila[3],
                sexo=fila[4],
                edad=fila[5],
                peso=fila[6],
                fecha_nacimiento=fila[7],
                estado=fila[8],
                id_usuario=id_usuario
            )
            mascotas.append(mascota)

        conn.close()
        return mascotas
    
    def obtener_mascota_por_id(self, id_mascota):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
        SELECT idMascota, nombre, especie, raza, sexo, edad, peso, fechaNacimiento, estado, idUsuario
        FROM Mascota 
        WHERE idMascota = ?
        """
        cursor.execute(query, (id_mascota,))

        fila = cursor.fetchone()

        if fila:
            mascota = Mascota(
                id_mascota=fila[0],
                nombre=fila[1],
                especie=fila[2],
                raza=fila[3],
                sexo=fila[4],
                edad=fila[5],
                peso=fila[6],
                fecha_nacimiento=fila[7],
                estado=fila[8],
                id_usuario=fila[9]
            )
            conn.close()
            return mascota

        conn.close()
        return None
    
    def actualizar_mascota(self, mascota):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            UPDATE Mascota
            SET nombre = ?, especie = ?, raza = ?, sexo = ?, edad = ?, peso = ?, fechaNacimiento = ?, estado = ?
            WHERE idMascota = ? AND idUsuario = ?
        """

        cursor.execute(query, (
            mascota.nombre,
            mascota.especie,
            mascota.raza,
            mascota.sexo,
            mascota.edad,
            mascota.peso,
            mascota.fecha_nacimiento,
            mascota.estado,
            mascota.id,
            mascota.id_usuario
        ))

        conn.commit()
        conn.close()

    def eliminar_mascota(self, id_mascota, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            DELETE FROM Mascota 
            WHERE idMascota = ? AND idUsuario = ?
        """
        cursor.execute(query, (id_mascota, id_usuario))

        conn.commit()
        conn.close()