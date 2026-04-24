import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from utils.auth import login_required, rol_required
from controllers.dashboard_controller import (
    dashboard_cliente,
    dashboard_clinica
)
from controllers.usuario_controller import (
    login,
    register,
    perfil,
    editar_perfil,
    eliminar_cuenta
)
from controllers.mascota_controller import (
    registrar_mascota,
    visualizar_mascotas,
    editar_mascota,
    eliminar_mascota
)
from controllers.clinica_controller import (
    registrar_clinica,
    editar_clinica,
    eliminar_clinica,
    visualizar_clinicas
)
from controllers.servicio_controller import (
    registrar_servicio,
    visualizar_servicios,
    editar_servicio,
    eliminar_servicio,
    servicios_por_clinica
)
from controllers.cita_controller import (
    registrar_cita,
    visualizar_citas,
    editar_cita,
    cancelar_cita,
    historial_citas,
    visualizar_citas_clinica,
    confirmar_cita
)

def cargar_env():
    if os.path.exists(".env"):  
        with open(".env") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

cargar_env()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth")
def auth():
    return render_template("auth.html")

app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/register", view_func=register, methods=['POST'])

##################
# RUTAS USUARIO
##################

@app.route("/dashboard_cliente")
@login_required
@rol_required("cliente")
def dashboard_cliente_ruta():
    return dashboard_cliente()

@app.route("/dashboard_clinica")
@login_required
@rol_required("clinica")
def dashboard_clinica_ruta():
    return dashboard_clinica()

@app.route("/perfil")
@login_required
def perfil_ruta():
    return perfil()

@app.route("/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil_ruta():
    return editar_perfil()

@app.route("/eliminar_cuenta", methods=["POST"])
@login_required
def eliminar_cuenta_ruta():
    return eliminar_cuenta()

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

##################
# RUTAS MASCOTA
##################

@app.route("/registrar_mascota", methods=["GET", "POST"])
@login_required
@rol_required("cliente")
def registrar_mascota_ruta():
    return registrar_mascota()

@app.route("/visualizar_mascotas")
@login_required
@rol_required("cliente")
def visualizar_mascotas_ruta():
    return visualizar_mascotas()

@app.route("/editar_mascota/<int:id_mascota>", methods=["GET", "POST"])
@login_required
@rol_required("cliente")
def editar_mascota_ruta(id_mascota):
    return editar_mascota(id_mascota)

@app.route("/eliminar_mascota/<int:id_mascota>", methods=["POST"])
@login_required
@rol_required("cliente")
def eliminar_mascota_ruta(id_mascota):
    return eliminar_mascota(id_mascota)

##################
# RUTAS CLINICA
##################

@app.route("/registrar_clinica", methods=["GET", "POST"])
@login_required
@rol_required("clinica")
def registrar_clinica_ruta():
    return registrar_clinica()

@app.route("/editar_clinica", methods=["GET", "POST"])
@login_required
@rol_required("clinica")
def editar_clinica_ruta():
    return editar_clinica()

@app.route("/eliminar_clinica", methods=["POST"])
@login_required
@rol_required("clinica")
def eliminar_clinica_ruta():
    return eliminar_clinica()

@app.route("/visualizar_clinicas")
@login_required
@rol_required("cliente")
def visualizar_clinicas_ruta():
    return visualizar_clinicas()


##################
# RUTAS SERVICIO
##################

@app.route("/registrar_servicio", methods=["GET", "POST"])
@login_required
@rol_required("clinica")
def registrar_servicio_ruta():
    return registrar_servicio()

@app.route("/visualizar_servicios")
@login_required
@rol_required("clinica")
def visualizar_servicios_ruta():
    return visualizar_servicios()

@app.route("/editar_servicio/<int:id_servicio>", methods=["GET", "POST"])
@login_required
@rol_required("clinica")
def editar_servicio_ruta(id_servicio):
    return editar_servicio(id_servicio)

@app.route("/eliminar_servicio/<int:id_servicio>", methods=["POST"])
@login_required
@rol_required("clinica")
def eliminar_servicio_ruta(id_servicio):
    return eliminar_servicio(id_servicio)

@app.route("/servicios_por_clinica/<int:id_clinica>")
@login_required
@rol_required("cliente")
def servicios_por_clinica_ruta(id_clinica):
    return servicios_por_clinica(id_clinica)

##################
# RUTAS CITA
##################

@app.route("/registrar_cita", methods=["GET", "POST"])
@login_required
@rol_required("cliente")
def registrar_cita_ruta():
    return registrar_cita()

@app.route("/visualizar_citas")
@login_required
@rol_required("cliente")
def visualizar_citas_ruta():
    return visualizar_citas()

@app.route("/editar_cita/<int:id_cita>", methods=["GET", "POST"])
@login_required
@rol_required("cliente")
def editar_cita_ruta(id_cita):
    return editar_cita(id_cita)

@app.route("/cancelar_cita/<int:id_cita>", methods=["POST"])
@login_required
@rol_required("cliente")
def cancelar_cita_ruta(id_cita):
    return cancelar_cita(id_cita)

@app.route("/historial_citas")
@login_required
@rol_required("cliente")
def historial_citas_ruta():
    return historial_citas()

@app.route("/citas_clinica")
@login_required
@rol_required("clinica")
def visualizar_citas_clinica_ruta():
    return visualizar_citas_clinica()

@app.route("/confirmar_cita/<int:id_cita>", methods=["POST"])
@login_required
@rol_required("clinica")
def confirmar_cita_ruta(id_cita):
    return confirmar_cita(id_cita)

if __name__ == '__main__':
    app.run()