import sqlite3
from models.cita_model import Cita

Datos = "database/sac.db"

class CitaDAO:

    def registrar_cita(self, cita):

        conn = sqlite3.connect(Datos)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO Cita (
                    fecha, observaciones, estado, idUsuario, idMascota, idClinica, idServicio
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                cita.fecha,
                cita.observaciones,
                cita.estado,
                cita.id_usuario,
                cita.id_mascota,
                cita.id_clinica,
                cita.id_servicio
            ))

            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print("Error de integridad:", e)
            conn.rollback()
            return False

        finally:
            conn.close()

    def obtener_citas_por_usuario(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
        SELECT 
            c.idCita,
            c.fecha,
            c.observaciones,
            c.estado,
            m.nombre,
            cl.nombre,
            s.nombre
        FROM Cita c
        LEFT JOIN Mascota m ON c.idMascota = m.idMascota
        LEFT JOIN Clinica cl ON c.idClinica = cl.idClinica
        LEFT JOIN Servicio s ON c.idServicio = s.idServicio
        WHERE c.idUsuario = ?
        ORDER BY c.fecha DESC
        """

        cursor.execute(query, (id_usuario,))
        filas = cursor.fetchall()

        conn.close()
        return filas
    
    def obtener_cita_por_id(self, id_cita):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idCita, fecha, observaciones, estado, idUsuario, idMascota, idClinica, idServicio
            FROM Cita
            WHERE idCita = ?
        """

        cursor.execute(query, (id_cita,))
        fila = cursor.fetchone()

        if fila:
            cita = Cita(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6],
                fila[7]
            )
            conn.close()
            return cita

        conn.close()
        return None
    
    def verificar_disponibilidad(self, id_clinica, fecha, id_cita=None):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        if id_cita:
            # 🔹 Para actualización (excluir la misma cita)
            query = """
                SELECT idUsuario
                FROM Cita
                WHERE idClinica = ? AND fecha = ? AND idCita != ? AND estado != 'Cancelada'
            """
            cursor.execute(query, (id_clinica, fecha, id_cita))
        else:
            # 🔹 Para registro
            query = """
                SELECT idUsuario
                FROM Cita
                WHERE idClinica = ? AND fecha = ? AND estado != 'Cancelada'
            """
            cursor.execute(query, (id_clinica, fecha))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]  # Retorna el ID del usuario que tiene la cita en ese horario

        return None
    
    def actualizar_cita(self, cita):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            UPDATE Cita
            SET fecha = ?, observaciones = ?
            WHERE idCita = ? AND idUsuario = ?
        """

        cursor.execute(query, (
            cita.fecha,
            cita.observaciones,
            cita.id,
            cita.id_usuario
        ))

        conn.commit()
        conn.close()

        return True
    
    def cancelar_cita(self, id_cita, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            UPDATE Cita
            SET estado = 'Cancelada'
            WHERE idCita = ? AND idUsuario = ?
        """

        cursor.execute(query, (id_cita, id_usuario))

        conn.commit()
        conn.close()

        return True
    
    def obtener_historial_citas(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT 
                c.idCita,
                c.fecha,
                c.observaciones,
                c.estado,
                m.nombre,
                cl.nombre,
                s.nombre
            FROM Cita c
            LEFT JOIN Mascota m ON c.idMascota = m.idMascota
            LEFT JOIN Clinica cl ON c.idClinica = cl.idClinica
            LEFT JOIN Servicio s ON c.idServicio = s.idServicio
            WHERE c.idUsuario = ? AND c.estado = 'Confirmada'
            ORDER BY c.fecha DESC
        """

        cursor.execute(query, (id_usuario,))
        filas = cursor.fetchall()

        conn.close()
        return filas
    
    def obtener_citas_por_clinica(self, id_clinica):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT 
                c.idCita,
                c.fecha,
                c.observaciones,
                c.estado,
                m.nombre,
                u.nombreCompleto,
                s.nombre
            FROM Cita c
            LEFT JOIN Mascota m ON c.idMascota = m.idMascota
            LEFT JOIN Usuario u ON c.idUsuario = u.idUsuario
            LEFT JOIN Servicio s ON c.idServicio = s.idServicio
            WHERE c.idClinica = ?
            ORDER BY c.fecha DESC
        """

        cursor.execute(query, (id_clinica,))
        filas = cursor.fetchall()

        conn.close()
        return filas
    
    def actualizar_estado_cita(self, id_cita, id_clinica, nuevo_estado):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            UPDATE Cita
            SET estado = ?
            WHERE idCita = ? AND idClinica = ?
        """

        cursor.execute(query, (nuevo_estado, id_cita, id_clinica))

        conn.commit()
        conn.close()

        return True