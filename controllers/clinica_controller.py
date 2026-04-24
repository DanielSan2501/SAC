from flask import render_template, request, session, redirect, url_for, flash
from models.clinica_model import Clinica
from dao.clinica_dao import ClinicaDAO

def registrar_clinica():

    if request.method == "POST":

        dao = ClinicaDAO()
        id_usuario = session["usuario"]["id"]

        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        correo = request.form.get("correo")

        if dao.existe_clinica_usuario(id_usuario):
            flash("Ya tienes una clínica registrada ❌", "error")
            return redirect(url_for("registrar_clinica_ruta"))

        clinica = Clinica(
            None,
            nombre,
            direccion,
            telefono,
            correo,
            0,  #SIEMPRE inicia NO verificada
            id_usuario
        )

        errores = clinica.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return redirect(url_for("registrar_clinica_ruta"))

        resultado = dao.registrar_clinica(clinica)

        if resultado == "fk_error":
            flash("Error de asociacion: el usuario no existe ❌ o es invalido", "error")
            return redirect(url_for("registrar_clinica_ruta"))

        if resultado is False:
            flash("Error al registrar la clínica ❌", "error")
            return redirect(url_for("registrar_clinica_ruta"))

        flash("Clínica registrada correctamente 🏥 (pendiente de validación)", "success")
        return redirect(url_for("dashboard_clinica_ruta"))

    return render_template("registrar_clinica.html")

def editar_clinica():

    dao = ClinicaDAO()
    id_usuario = session["usuario"]["id"]

    clinica = dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No tienes una clínica registrada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    if request.method == "POST":

        clinica.nombre = request.form.get("nombre")
        clinica.direccion = request.form.get("direccion")
        clinica.telefono = request.form.get("telefono")
        clinica.correo = request.form.get("correo")

        # 🔥 REGLA IMPORTANTE
        if clinica.estado == 1:
            clinica.estado = 0
            flash("La clínica será nuevamente validada tras los cambios ⏳", "warning")

        errores = clinica.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("editar_clinica.html", clinica=clinica)

        resultado = dao.actualizar_clinica(clinica)

        if resultado == "fk_error":
            flash("Error de integridad: el usuario no existe ❌ o es invalido", "error")
            return render_template("editar_clinica.html", clinica=clinica)

        if resultado is False:
            flash("Error al actualizar la clínica ❌", "error")
            return render_template("editar_clinica.html", clinica=clinica)

        # 🔥 actualizar sesión
        session["usuario"]["estado_clinica"] = clinica.estado

        flash("Clínica actualizada correctamente 🏥", "success")
        return redirect(url_for("editar_clinica_ruta"))

    return render_template("editar_clinica.html", clinica=clinica)

def eliminar_clinica():

    if "usuario" not in session:
        return redirect(url_for("index"))

    id_usuario = session["usuario"]["id"]

    dao = ClinicaDAO()
    exito = dao.eliminar_clinica_por_usuario(id_usuario)

    if exito:
        # 🔥 limpiar estado en sesión
        session["usuario"]["estado_clinica"] = None

        flash("Clínica eliminada correctamente 🗑️", "success")
    elif exito == "fk_error":
        flash("Error de integridad: No se puede eliminar la clínica porque tiene citas asociadas ❌", "error")
    else:
        flash("Error al eliminar la clínica ❌", "error")

    return redirect(url_for("dashboard_clinica_ruta"))

def visualizar_clinicas():

    dao = ClinicaDAO()
    clinicas = dao.obtener_clinicas_activas()

    return render_template("visualizar_clinicas.html", clinicas=clinicas)