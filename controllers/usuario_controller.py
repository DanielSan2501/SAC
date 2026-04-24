from flask import render_template, request, session, redirect, url_for, flash
from dao.usuario_dao import UsuarioDAO
from dao.clinica_dao import ClinicaDAO
from models.usuario_model import Usuario

# =========================
# LOGIN
# =========================

def login():

    if "usuario" in session:
        if session["usuario"]["rol"] == "cliente":
            return redirect(url_for("dashboard_cliente_ruta"))
        return redirect(url_for("dashboard_clinica_ruta"))

    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        dao = UsuarioDAO()
        usuario = dao.validar_usuario_nuevo(correo, password)

        if usuario:
            session["usuario"] = {
                "id": usuario.id,
                "numero_documento": usuario.numero_documento,
                "nombre_completo": usuario.nombre_completo,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "estado": usuario.estado
            }

            if usuario.rol == "clinica":
                clinica = ClinicaDAO()
                estado_clinica = clinica.obtener_estado_clinica(usuario.id)
                session["usuario"]["estado_clinica"] = estado_clinica

            if usuario.rol == "cliente":
                return redirect(url_for("dashboard_cliente_ruta"))
            else:
                return redirect(url_for("dashboard_clinica_ruta"))
        else:
            flash("Correo o contraseña incorrectos ❌", "error")
            return redirect(url_for("auth", modo="login"))

    return redirect(url_for("auth", modo="login"))

# =========================
# REGISTER
# =========================

def register():

    if "usuario" in session:
        if session["usuario"]["rol"] == "cliente":
            return redirect(url_for("dashboard_cliente_ruta"))
        return redirect(url_for("dashboard_clinica_ruta"))

    if request.method == "POST":

        tipo_documento = request.form.get("tipo_documento")
        numero_documento = request.form.get("numero_documento")
        nombre_completo = request.form.get("nombre_completo")
        correo = request.form.get("correo")
        password = request.form.get("password")
        telefono = request.form.get("telefono")
        rol = request.form.get("rol")

        dao = UsuarioDAO()

        usuario = Usuario(
            None,
            tipo_documento,
            numero_documento,
            nombre_completo,
            correo,
            password,
            telefono,
            rol,
            None,
            1
        )

        errores = usuario.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return redirect(url_for("auth", modo="register"))
        
        if dao.validar_numero_documento(numero_documento):
            flash("El número de documento ya está registrado ❌", "error")
            return redirect(url_for("auth", modo="register"))

        if dao.existe_correo(correo):
            flash("El correo ya está registrado ❌", "error")
            return redirect(url_for("auth", modo="register"))

        dao.crear_usuario(usuario)
        
        flash("Usuario registrado exitosamente ✅", "success")
        return redirect(url_for("auth", modo="login"))

    return redirect(url_for("auth", modo="register"))

# =========================
# VER PERFIL
# =========================

def perfil():

    if "usuario" not in session:
        return redirect(url_for("index"))

    dao = UsuarioDAO()
    id_usuario = session["usuario"]["id"]
    usuario = dao.obtener_usuario_por_id(id_usuario)
    return render_template("perfil.html", usuario=usuario)

# =========================
# EDITAR PERFIL
# =========================

def editar_perfil():

    if "usuario" not in session:
        return redirect(url_for("index"))
    
    dao = UsuarioDAO()
    id_usuario = session["usuario"]["id"]
    usuario = dao.obtener_usuario_por_id(id_usuario)

    if request.method == "POST":
        
        tipo_documento = request.form.get("tipo_documento")
        numero_documento = request.form.get("numero_documento")
        nombre_completo = request.form.get("nombre_completo")
        correo = request.form.get("correo")
        password = request.form.get("password")
        telefono = request.form.get("telefono")
        estado = request.form.get("estado")

        usuario = Usuario(
            id_usuario,
            tipo_documento,
            numero_documento,
            nombre_completo,
            correo,
            password,
            telefono,
            session["usuario"]["rol"],
            None,
            estado
        )

        errores = usuario.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("editar_perfil.html", usuario=usuario)
        
        dao.actualizar_usuario(usuario)

        session["usuario"]["nombre_completo"] = nombre_completo
        session["usuario"]["correo"] = correo

        flash("Perfil actualizado correctamente ✅", "success")

    return render_template("editar_perfil.html", usuario=usuario)

# =========================
# ELIMINAR USUARIO
# =========================

def eliminar_cuenta():
    
    if "usuario" not in session:
        return redirect(url_for("index"))
    
    id_usuario = session["usuario"]["id"]

    dao = UsuarioDAO()
    exito = dao.eliminar_usuario(id_usuario)

    if exito:
        session.clear()
        flash("Cuenta eliminada correctamente ✅", "success")
        return redirect(url_for("index"))
    else:
        flash("Error al eliminar la cuenta ❌", "error")
        return redirect(url_for("perfil"))

