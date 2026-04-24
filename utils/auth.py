from flask import session, redirect, url_for, flash, render_template
from functools import wraps
from dao.clinica_dao import ClinicaDAO

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "usuario" not in session:
            return redirect(url_for("index"))
        
        if session["usuario"]["rol"] == "clinica":
            dao = ClinicaDAO()
            estado = dao.obtener_estado_clinica(session["usuario"]["id"])
            session["usuario"]["estado_clinica"] = estado

        return func(*args, **kwargs)

    return wrapper

def rol_required(rol_permitido):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if "usuario" not in session:
                return redirect(url_for("index"))

            if session["usuario"]["rol"] != rol_permitido:
                flash("No tienes permiso para acceder a esta página ❌", "error")
                return redirect(url_for("index"))

            return func(*args, **kwargs)

        return wrapper

    return decorator