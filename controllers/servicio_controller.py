from flask import render_template, request, session, redirect, url_for, flash, jsonify
from models.servicio_model import Servicio
from dao.servicio_dao import ServicioDAO
from dao.clinica_dao import ClinicaDAO

def registrar_servicio():

    if request.method == "POST":

        dao = ServicioDAO()
        clinica_dao = ClinicaDAO()

        id_usuario = session["usuario"]["id"]

        clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

        if not clinica:
            flash("No tienes una clínica registrada ❌", "error")
            return redirect(url_for("dashboard_clinica_ruta"))
        
        session["usuario"]["estado_clinica"] = clinica.estado

        if clinica.estado != 1:
            flash("Tu clínica no está validada ❌", "error")
            return redirect(url_for("dashboard_clinica_ruta"))

        tipo_servicio = request.form.get("tipo_servicio")
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        duracion = request.form.get("duracion")

        servicio = Servicio(
            None,
            tipo_servicio,
            nombre,
            descripcion,
            precio,
            duracion,
            1,  # estado activo por defecto
            clinica.id
        )

        errores = servicio.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return redirect(url_for("registrar_servicio_ruta"))

        resultado = dao.registrar_servicio(servicio)

        if resultado == "fk_error":
            flash("Error de asociación: la clínica no existe ❌ o es inválida", "error")
            return redirect(url_for("registrar_servicio_ruta"))

        if resultado is False:
            flash("Error al registrar el servicio ❌", "error")
            return redirect(url_for("registrar_servicio_ruta"))

        flash("Servicio registrado correctamente 🧪", "success")
        return redirect(url_for("registrar_servicio_ruta"))

    return render_template("registrar_servicio.html")

def visualizar_servicios():

    dao = ServicioDAO()
    clinica_dao = ClinicaDAO()

    id_usuario = session["usuario"]["id"]

    clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No tienes una clínica registrada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    if clinica.estado != 1:
        flash("Tu clínica no está validada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    servicios = dao.obtener_servicios_por_clinica(clinica.id)

    return render_template("visualizar_servicios.html", servicios=servicios)

def editar_servicio(id_servicio):

    dao = ServicioDAO()
    clinica_dao = ClinicaDAO()

    id_usuario = session["usuario"]["id"]

    clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No tienes una clínica registrada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    if clinica.estado != 1:
        flash("Tu clínica no está validada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    servicio = dao.obtener_servicio_por_id(id_servicio)

    if not servicio:
        flash("Servicio no encontrado ❌", "error")
        return redirect(url_for("visualizar_servicios_ruta"))

    if servicio.id_clinica != clinica.id:
        flash("No tienes permiso para editar este servicio ❌", "error")
        return redirect(url_for("visualizar_servicios_ruta"))

    if request.method == "POST":

        tipo_servicio = request.form.get("tipo_servicio")
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion") or None
        precio = request.form.get("precio")
        duracion = request.form.get("duracion")
        estado = int(request.form.get("estado"))

        servicio = Servicio(
            id_servicio,
            tipo_servicio,
            nombre,
            descripcion,
            precio,
            duracion,
            estado,
            clinica.id
        )

        errores = servicio.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("editar_servicio.html", servicio=servicio)

        resultado = dao.actualizar_servicio(servicio)

        if resultado == "fk_error":
            flash("Error de asociación: la clínica no existe ❌ o es inválida", "error")
            return render_template("editar_servicio.html", servicio=servicio)

        flash("Servicio actualizado correctamente 🧪", "success")
        return redirect(url_for("visualizar_servicios_ruta"))

    return render_template("editar_servicio.html", servicio=servicio)

def eliminar_servicio(id_servicio):

    dao = ServicioDAO()
    clinica_dao = ClinicaDAO()

    id_usuario = session["usuario"]["id"]

    clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No tienes una clínica registrada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    if clinica.estado != 1:
        flash("Tu clínica no está validada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    servicio = dao.obtener_servicio_por_id(id_servicio)

    if not servicio:
        flash("Servicio no encontrado ❌", "error")
        return redirect(url_for("visualizar_servicios_ruta"))

    if servicio.id_clinica != clinica.id:
        flash("No tienes permiso para eliminar este servicio ❌", "error")
        return redirect(url_for("visualizar_servicios_ruta"))

    resultado = dao.eliminar_servicio(id_servicio, clinica.id)

    if resultado == "fk_error":
        flash("Error de asociación: la clínica no existe ❌ o es inválida", "error")
        return redirect(url_for("visualizar_servicios_ruta"))
    
    if resultado is False:
        flash("Error al desactivar el servicio ❌", "error")
        return redirect(url_for("visualizar_servicios_ruta"))

    flash("Servicio desactivado correctamente 🗑️", "success")
    return redirect(url_for("visualizar_servicios_ruta"))

def servicios_por_clinica(id_clinica):

    dao = ServicioDAO()
    servicios = dao.obtener_servicios_activos(id_clinica)

    resultado = []

    for s in servicios:
        resultado.append({
            "id": s.id,
            "nombre": s.nombre
        })

    return jsonify({"servicios": resultado})