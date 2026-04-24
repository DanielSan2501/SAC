class Cita:
    
    def __init__(self, id_cita, fecha, observaciones, estado, id_usuario, id_mascota, id_clinica, id_servicio):

        self.id = id_cita
        self.fecha = fecha
        self.observaciones = observaciones
        self.estado = estado
        self.id_usuario = id_usuario
        self.id_mascota = id_mascota
        self.id_clinica = id_clinica
        self.id_servicio = id_servicio

    def validar_datos(self):

        errores = []

        if not self.fecha or str(self.fecha).strip() == "":
            errores.append("La fecha es obligatoria.")

        estados_validos = ["Pendiente", "Confirmada", "Cancelada"]
        if not self.estado:
            errores.append("El estado es obligatorio.")
        elif self.estado not in estados_validos:
            errores.append("El estado de la cita no es válido.")

        if not self.id_usuario or self.id_usuario <= 0:
            errores.append("El ID del usuario es obligatorio.")

        if not self.id_mascota or self.id_mascota <= 0:
            errores.append("El ID de la mascota es obligatorio.")

        if not self.id_clinica or self.id_clinica <= 0:
            errores.append("El ID de la clínica es obligatorio.")

        if not self.id_servicio or self.id_servicio <= 0:
            errores.append("El ID del servicio es obligatorio.")

        if self.observaciones is None:
            self.observaciones = ""

        return errores