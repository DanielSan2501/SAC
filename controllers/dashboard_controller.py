from flask import render_template, session, redirect, url_for
from dao.clinica_dao import ClinicaDAO
from dao.mascota_dao import MascotaDAO
from dao.cita_dao import CitaDAO

def dashboard_cliente():

    if "usuario" not in session:
        return redirect(url_for("index"))
    
    id_usuario = session["usuario"]["id"]

    mascota_dao = MascotaDAO()
    cita_dao = CitaDAO()

    mascotas = mascota_dao.obtener_mascotas_por_usuario(id_usuario)
    citas = cita_dao.obtener_citas_por_usuario(id_usuario)

    # 🔥 contar pendientes
    citas_pendientes = 0
    for c in citas:
        if c[3] == "Pendiente":
            citas_pendientes += 1

    return render_template(
        "dashboard_cliente.html",
        usuario=session["usuario"],
        mascotas=mascotas,
        citas=citas,
        citas_pendientes=citas_pendientes
    )


def dashboard_clinica():

    if "usuario" not in session:
        return redirect(url_for("index"))

    dao = ClinicaDAO()
    cita_dao = CitaDAO()

    id_usuario = session["usuario"]["id"]

    estado = dao.obtener_estado_clinica(id_usuario)
    session["usuario"]["estado_clinica"] = estado

    clinica = dao.obtener_clinica_por_usuario(id_usuario)

    citas = []
    citas_pendientes = 0
    citas_confirmadas = 0

    if clinica:
        citas = cita_dao.obtener_citas_por_clinica(clinica.id)

        for c in citas:
            if c[3] == "Pendiente":
                citas_pendientes += 1
            elif c[3] == "Confirmada":
                citas_confirmadas += 1

    return render_template(
        "dashboard_clinica.html",
        usuario=session["usuario"],
        citas=citas,
        citas_pendientes=citas_pendientes,
        citas_confirmadas=citas_confirmadas
    )