class Clinica:

    def __init__(self, id_clinica, nombre, direccion, telefono, correo, estado, id_usuario):
        self.id = id_clinica
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.estado = estado
        self.id_usuario = id_usuario

    def validar_datos(self):

        errores = []

        if not self.nombre or not all(c.isalpha() or c.isspace() for c in self.nombre):
            errores.append("El nombre de la clínica es obligatorio y solo puede contener letras y espacios.")

        if not self.direccion or len(self.direccion.strip()) == 0:
            errores.append("La dirección es obligatoria.")

        if not self.telefono or not self.telefono.isdigit():
            errores.append("El teléfono es obligatorio y debe ser numérico.")
        elif len(self.telefono) < 8 or len(self.telefono) > 13:
            errores.append("El teléfono debe tener entre 8 y 13 dígitos.")

        if not self.correo or "@" not in self.correo:
            errores.append("El correo no es válido.")

        return errores