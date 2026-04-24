from flask import render_template, request, session, redirect, url_for, flash
from models.cita_model import Cita
from dao.cita_dao import CitaDAO
from dao.mascota_dao import MascotaDAO
from dao.clinica_dao import ClinicaDAO
from dao.servicio_dao import ServicioDAO

def registrar_cita():

    dao = CitaDAO()
    mascota_dao = MascotaDAO()
    clinica_dao = ClinicaDAO()
    servicio_dao = ServicioDAO()

    id_usuario = session["usuario"]["id"]

    # 🔹 Obtener datos para selects
    mascotas = mascota_dao.obtener_mascotas_por_usuario(id_usuario)
    clinicas = clinica_dao.obtener_clinicas_activas()
    servicios = []  

    if request.method == "POST":

        if not request.form.get("id_mascota"):
            flash("Debes seleccionar una mascota ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        if not request.form.get("id_clinica"):
            flash("Debes seleccionar una clínica ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        if not request.form.get("id_servicio"):
            flash("Debes seleccionar un servicio ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        id_clinica = int(request.form.get("id_clinica"))
        id_mascota = int(request.form.get("id_mascota"))
        id_servicio = int(request.form.get("id_servicio"))
        fecha = request.form.get("fecha").replace("T", " ")
        observaciones = request.form.get("observaciones")

        # 🔥 VALIDACIÓN IMPORTANTE: mascota pertenece al usuario
        mascotas_usuario = mascota_dao.obtener_mascotas_por_usuario(id_usuario)
        ids_mascotas = [m.id for m in mascotas_usuario]

        if id_mascota not in ids_mascotas:
            flash("Mascota inválida ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        # 🔹 Crear objeto
        cita = Cita(
            None,
            fecha,
            observaciones,
            "Pendiente",
            id_usuario,
            id_mascota,
            id_clinica,
            id_servicio
        )

        errores = cita.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)
        
        disponible = dao.verificar_disponibilidad(
            id_clinica,
            fecha
        )

        if disponible:
            if disponible == id_usuario:
                flash("No puedes agendar dos citas en la misma fecha y hora ❌", "error")
                return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)
            else:
                flash("Ese horario ya está ocupado en la clínica ❌", "error")
                return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        resultado = dao.registrar_cita(cita)

        if resultado == "fk_error":
            flash("Error de asociación en la cita ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        if resultado is False:
            flash("Error al registrar la cita ❌", "error")
            return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

        flash("Cita agendada correctamente 📅", "success")
        return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

    return render_template("registrar_cita.html", mascotas=mascotas, clinicas=clinicas, servicios=servicios)

def visualizar_citas():

    dao = CitaDAO()

    id_usuario = session["usuario"]["id"]

    citas = dao.obtener_citas_por_usuario(id_usuario)

    return render_template("visualizar_citas.html", citas=citas)

def editar_cita(id_cita):

    dao = CitaDAO()
    id_usuario = session["usuario"]["id"]

    cita = dao.obtener_cita_por_id(id_cita)

    if not cita or cita.id_usuario != id_usuario:
        flash("Cita no válida ❌", "error")
        return redirect(url_for("visualizar_citas_ruta"))

    if request.method == "POST":

        fecha = request.form.get("fecha").replace("T", " ")
        observaciones = request.form.get("observaciones")

        cita.fecha = fecha
        cita.observaciones = observaciones

        errores = cita.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("editar_cita.html", cita=cita)
        
        # 🔥 Validar disponibilidad
        disponible = dao.verificar_disponibilidad(
            cita.id_clinica,
            fecha,
            cita.id
        )

        if disponible:
            if disponible == id_usuario:
                flash("No puedes reprogramar a un horario donde ya tienes otra cita ❌", "error")
                return render_template("editar_cita.html", cita=cita)
            else:
                flash("La clínica ya tiene una cita en esa fecha y hora ❌", "error")
                return render_template("editar_cita.html", cita=cita)

        dao.actualizar_cita(cita)

        flash("Cita reprogramada correctamente 📅", "success")
        return render_template("editar_cita.html", cita=cita)

    return render_template("editar_cita.html", cita=cita)

def cancelar_cita(id_cita):

    dao = CitaDAO()
    id_usuario = session["usuario"]["id"]

    cita = dao.obtener_cita_por_id(id_cita)

    if not cita or cita.id_usuario != id_usuario:
        flash("Cita no válida ❌", "error")
        return redirect(url_for("visualizar_citas_ruta"))

    resultado = dao.cancelar_cita(id_cita, id_usuario)

    if resultado is False:
        flash("Error al cancelar la cita ❌", "error")
        return redirect(url_for("visualizar_citas_ruta"))

    flash("Cita cancelada correctamente ❌", "success")
    return redirect(url_for("visualizar_citas_ruta"))

def historial_citas():

    dao = CitaDAO()
    id_usuario = session["usuario"]["id"]

    citas = dao.obtener_historial_citas(id_usuario)

    return render_template("historial_citas.html", citas=citas)

def visualizar_citas_clinica():

    dao = CitaDAO()
    clinica_dao = ClinicaDAO()

    id_usuario = session["usuario"]["id"]

    clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No tienes clínica registrada ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    citas = dao.obtener_citas_por_clinica(clinica.id)

    return render_template("citas_clinica.html", citas=citas)

def confirmar_cita(id_cita):

    dao = CitaDAO()
    clinica_dao = ClinicaDAO()

    id_usuario = session["usuario"]["id"]
    clinica = clinica_dao.obtener_clinica_por_usuario(id_usuario)

    if not clinica:
        flash("No autorizado ❌", "error")
        return redirect(url_for("dashboard_clinica_ruta"))

    dao.actualizar_estado_cita(id_cita, clinica.id, "Confirmada")

    flash("Cita confirmada ✔", "success")
    return redirect(url_for("visualizar_citas_clinica_ruta"))