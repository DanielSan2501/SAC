import sqlite3
from models.usuario_model import Usuario

Datos = "database/sac.db"

class UsuarioDAO:
        
    # Metodo para validar el login del usuario, verificando correo, contraseña y estado activo (1)
    def validar_usuario_nuevo(self, correo, password):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT * FROM Usuario WHERE correo = ? AND contraseña = ? AND estado = 1"
        cursor.execute(query, (correo, password))

        fila = cursor.fetchone()

        conn.close()

        if fila:
            usuario = Usuario(
                fila[0], #idUsuario
                fila[1], #tipo_documento
                fila[2], #numero_documento
                fila[3], #nombre_completo
                fila[4], #correo
                fila[5], #password
                fila[6], #telefono
                fila[7], #rol
                fila[8], #fecha_registro
                fila[9]  #estado
                )
            return usuario
        else:
            return None
        
    # Metodo para crear un nuevo usuario en la base de datos
    def crear_usuario(self, usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            INSERT INTO Usuario 
            (tipoDocumento, numeroDocumento, nombreCompleto, correo, contraseña, 
            telefono, rol, fechaRegistro, estado) 
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'), 1)
        """
        cursor.execute(query, (
            usuario.tipo_documento,
            usuario.numero_documento,
            usuario.nombre_completo,
            usuario.correo,
            usuario.password,
            usuario.telefono,
            usuario.rol
            ))

        conn.commit()
        conn.close()

    def validar_numero_documento(self, numero_documento):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT 1 FROM Usuario WHERE numeroDocumento = ?"
        cursor.execute(query, (numero_documento,))

        resultado = cursor.fetchone()

        conn.close()

        return resultado is not None

    def existe_correo(self, correo):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = "SELECT 1 FROM Usuario WHERE correo = ?"
        cursor.execute(query, (correo,))

        resultado = cursor.fetchone()

        conn.close()

        return resultado is not None
    
    def obtener_usuario_por_id(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            SELECT idUsuario, tipoDocumento, numeroDocumento, nombreCompleto,
            correo, contraseña, telefono, rol, fechaRegistro, estado 
            FROM Usuario 
            WHERE idUsuario = ?
        """
        cursor.execute(query, (id_usuario,))

        fila = cursor.fetchone()

        conn.close()

        if fila:
            return Usuario(
                fila[0], #idUsuario
                fila[1], #tipo_documento
                fila[2], #numero_documento
                fila[3], #nombre_completo
                fila[4], #correo
                fila[5], #password
                fila[6], #telefono
                fila[7], #rol
                fila[8], #fecha_registro
                fila[9]  #estado
                )
        else:
            return None
        
    def actualizar_usuario(self, usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        query = """
            UPDATE Usuario 
            SET tipoDocumento = ?, numeroDocumento = ?, nombreCompleto = ?, 
            correo = ?, contraseña = ?, telefono = ?, estado = ? 
            WHERE idUsuario = ?
        """
        cursor.execute(query, (
            usuario.tipo_documento,
            usuario.numero_documento,
            usuario.nombre_completo,
            usuario.correo,
            usuario.password,
            usuario.telefono,
            usuario.estado,
            usuario.id
        ))

        conn.commit()
        conn.close()

    def eliminar_usuario(self, id_usuario):

        conn = sqlite3.connect(Datos)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        try:
            query = "DELETE FROM Usuario WHERE idUsuario = ?"
            cursor.execute(query, (id_usuario,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()