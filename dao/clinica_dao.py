import sqlite3
from models.clinica_model import Clinica

Datos = "database/sac.db"

class ClinicaDAO:

    def existe_clinica_usuario(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT 1 FROM Clinica WHERE idUsuario = ? LIMIT 1"
        cursor.execute(query, (id_usuario,))

        resultado = cursor.fetchone()
        conn.close()

        return resultado is not None


    def registrar_clinica(self, clinica):

        conn = sqlite3.connect(Datos)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        try:
            
            query = """
                INSERT INTO Clinica (
                    nombre, direccion, telefono, correo, estado, idUsuario
                ) VALUES (?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                clinica.nombre,
                clinica.direccion,
                clinica.telefono,
                clinica.correo,
                clinica.estado, # El estado es 0 por defecto al registrar una clínica, lo que indica que está pendiente de aprobación
                clinica.id_usuario
            ))

            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print("Error de integridad:", e)
            conn.rollback()
            return False

        finally:
            conn.close()

    def obtener_estado_clinica(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT estado FROM Clinica WHERE idUsuario = ? LIMIT 1"
        cursor.execute(query, (id_usuario,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]  
        else:
            return None  
        
    def obtener_clinica_por_usuario(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idClinica, nombre, direccion, telefono, correo, estado, idUsuario
            FROM Clinica 
            WHERE idUsuario = ?
        """
        cursor.execute(query, (id_usuario,))

        fila = cursor.fetchone()

        if fila:
            clinica = Clinica(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6]
            )
            conn.close()
            return clinica
        
        conn.close()
        return None
        
    def actualizar_clinica(self, clinica):
        
        conn = sqlite3.connect(Datos)
        
        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            conn.close()
            return "fk_error"

        cursor = conn.cursor()

        query = """
            UPDATE Clinica
            SET nombre = ?, direccion = ?, telefono = ?, correo = ?, estado = ?
            WHERE idClinica = ? AND idUsuario = ?
        """

        cursor.execute(query, (
            clinica.nombre,
            clinica.direccion,
            clinica.telefono,
            clinica.correo,
            clinica.estado,
            clinica.id,
            clinica.id_usuario
        ))

        conn.commit()
        conn.close()
        return True

    def eliminar_clinica_por_usuario(self, id_usuario):

        try:
            conn = sqlite3.connect(Datos)

            try:
                conn.execute("PRAGMA foreign_keys = ON")
            except Exception:
                conn.close()
                return "fk_error"

            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM Clinica
                WHERE idUsuario = ?
            """, (id_usuario,))

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print("Error al eliminar clínica:", e)
            return False
        
    def obtener_clinicas_activas(self):

        conn = sqlite3.connect(Datos)
        cursor = conn.cursor()

        query = """
            SELECT idClinica, nombre, direccion, telefono, correo, estado, idUsuario
            FROM Clinica
            WHERE estado = 1
        """

        cursor.execute(query)
        filas = cursor.fetchall()

        clinicas = []

        for fila in filas:
            clinica = Clinica(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6]
            )
            clinicas.append(clinica)

        conn.close()
        return clinicas
