import sqlite3
from models.servicio_model import Servicio

Datos = "database/sac.db"

class ServicioDAO:

    def validar_clinica_activa(self, id_clinica):

        conn = sqlite3.connect(Datos)
        cursor = conn.cursor()

        query = "SELECT estado FROM Clinica WHERE idClinica = ?"
        cursor.execute(query, (id_clinica,))

        fila = cursor.fetchone()

        if not fila:
            conn.close()
            return False

        if fila[0] != 1:
            conn.close()
            return False

        conn.close()
        return True
        
    def registrar_servicio(self, servicio):

        conn = sqlite3.connect(Datos)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        try:

            query = """
                INSERT INTO Servicio (
                    tipoServicio, nombre, descripcion, precio, duracion, estado, idClinica
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                servicio.tipo_servicio,
                servicio.nombre,
                servicio.descripcion,
                float(servicio.precio),
                int(servicio.duracion),
                servicio.estado,
                servicio.id_clinica
            ))

            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print("Error de integridad:", e)
            conn.rollback()
            return False

        finally:
            conn.close()

    def obtener_servicios_por_clinica(self, id_clinica):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idServicio, tipoServicio, nombre, descripcion, precio, duracion, estado, idClinica
            FROM Servicio 
            WHERE idClinica = ?
        """
        cursor.execute(query, (id_clinica,))

        filas = cursor.fetchall()
        servicios = []

        for fila in filas:
            servicio = Servicio(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6],
                fila[7]
            )
            servicios.append(servicio)

        conn.close()
        return servicios
    
    def obtener_servicio_por_id(self, id_servicio):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idServicio, tipoServicio, nombre, descripcion, precio, duracion, estado, idClinica
            FROM Servicio
            WHERE idServicio = ?
        """

        cursor.execute(query, (id_servicio,))
        fila = cursor.fetchone()

        if fila:
            servicio = Servicio(
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
            return servicio

        conn.close()
        return None
    
    def actualizar_servicio(self, servicio):

        conn = sqlite3.connect(Datos)
        
        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        query = """
            UPDATE Servicio
            SET tipoServicio = ?, nombre = ?, descripcion = ?, precio = ?, duracion = ?, estado = ?
            WHERE idServicio = ? AND idClinica = ?
        """

        cursor.execute(query, (
            servicio.tipo_servicio,
            servicio.nombre,
            servicio.descripcion,
            float(servicio.precio),
            int(servicio.duracion),
            servicio.estado,
            servicio.id,
            servicio.id_clinica
        ))

        conn.commit()
        conn.close()
        return True

    def eliminar_servicio(self, id_servicio, id_clinica):

        conn = sqlite3.connect(Datos)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        query = """
            UPDATE Servicio
            SET estado = 0
            WHERE idServicio = ? AND idClinica = ?
        """

        cursor.execute(query, (id_servicio, id_clinica))
        conn.commit()

        filas_afectadas = cursor.rowcount

        conn.close()

        return filas_afectadas > 0
    
    def obtener_servicios_activos(self, id_clinica):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idServicio, tipoServicio, nombre, descripcion, precio, duracion, estado, idClinica
            FROM Servicio
            WHERE idClinica = ? AND estado = 1
        """

        cursor.execute(query, (id_clinica,))
        filas = cursor.fetchall()

        servicios = []

        for fila in filas:
            servicio = Servicio(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6],
                fila[7]
            )
            servicios.append(servicio)

        conn.close()
        return servicios