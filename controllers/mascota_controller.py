from flask import render_template, request, session, redirect, url_for, flash
from models.mascota_model import Mascota
from dao.mascota_dao import MascotaDAO

def registrar_mascota():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        especie = request.form.get("especie")
        raza = request.form.get("raza") or None
        sexo = request.form.get("sexo")
        edad = request.form.get("edad") or None
        peso = request.form.get("peso")
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        id_usuario = session["usuario"]["id"]

        dao = MascotaDAO()

        mascota = Mascota(
            None,
            nombre,
            especie,
            raza,
            sexo,
            edad,
            peso,
            fecha_nacimiento,
            1,
            id_usuario
        )
        
        errores = mascota.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return redirect(url_for("registrar_mascota_ruta"))
        
        if dao.validar_mascota_registrada(nombre, id_usuario):
            flash("Ya tienes una mascota registrada con ese nombre ❌", "error")
            return redirect(url_for("registrar_mascota_ruta"))
        
        resultado = dao.registrar_mascota(mascota)

        if resultado == "fk_error":
            flash("Error de asociación: el usuario no existe ❌ o es inválido", "error")
            return redirect(url_for("registrar_mascota_ruta"))

        flash("Mascota registrada exitosamente ✅", "success")
        return redirect(url_for("registrar_mascota_ruta"))
    
    return render_template("registrar_mascota.html")

def visualizar_mascotas():

    id_usuario = session["usuario"]["id"]
    dao = MascotaDAO()
    mascotas = dao.obtener_mascotas_por_usuario(id_usuario)

    return render_template("visualizar_mascotas.html", mascotas=mascotas)

def editar_mascota(id_mascota):
    
    dao = MascotaDAO()
    id_usuario = session["usuario"]["id"]
    mascota = dao.obtener_mascota_por_id(id_mascota)

    if mascota.id_usuario != id_usuario:
        flash("No tienes permiso para editar esta mascota ❌", "error")
        return redirect(url_for("visualizar_mascotas_ruta"))
    
    if request.method == "POST":

        nombre = request.form.get("nombre")
        especie = request.form.get("especie")
        raza = request.form.get("raza") or None
        sexo = request.form.get("sexo")
        edad = request.form.get("edad") or None
        peso = request.form.get("peso")
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        estado = int(request.form.get("estado"))

        mascota = Mascota(
            id_mascota,
            nombre,
            especie,
            raza,
            sexo,
            edad,
            peso,
            fecha_nacimiento,
            estado,
            id_usuario
        )

        errores = mascota.validar_datos()

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("editar_mascota.html", mascota=mascota)
        
        dao.actualizar_mascota(mascota)
        flash("Mascota actualizada exitosamente ✅", "success")
    
    return render_template("editar_mascota.html", mascota=mascota)

def eliminar_mascota(id_mascota):

    dao = MascotaDAO()
    id_usuario = session["usuario"]["id"]
    mascota = dao.obtener_mascota_por_id(id_mascota)

    if not mascota or mascota.id_usuario != id_usuario:
        flash("No tienes permiso para eliminar esta mascota ❌", "error")
        return redirect(url_for("visualizar_mascotas_ruta"))
    
    dao.eliminar_mascota(id_mascota, id_usuario)

    flash("Mascota eliminada exitosamente ✅", "success")
    return redirect(url_for("visualizar_mascotas_ruta"))

