class Usuario:

    def __init__(self, id, tipo_documento, numero_documento, nombre_completo, correo, password, telefono, rol, fecha_registro, estado):

        self.id = id
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.password = password
        self.telefono = telefono
        self.rol = rol
        self.fecha_registro = fecha_registro
        self.estado = estado

    def validar_datos(self):

        errores = []

        if not self.tipo_documento:
            errores.append("El tipo de documento es obligatorio.")

        if not self.numero_documento or not self.numero_documento.isdigit():
            errores.append("El número de documento es obligatorio y debe ser numérico.")
        elif len(self.numero_documento) < 8 or len(self.numero_documento) > 15:
            errores.append("El número de documento debe tener entre 8 y 15 dígitos.")

        if not self.nombre_completo or not all(c.isalpha() or c.isspace() for c in self.nombre_completo):
            errores.append("El nombre completo es obligatorio y debe contener solo letras y espacios.")

        if not self.correo or "@" not in self.correo:
            errores.append("El correo es obligatorio y debe tener un formato válido.")

        if not self.password or len(self.password) < 8:
            errores.append("La contraseña es obligatoria y debe tener al menos 8 caracteres.")

        if not self.telefono or not self.telefono.isdigit():
            errores.append("El teléfono es obligatorio y debe ser numérico.")
        elif len(self.telefono) < 8 or len(self.telefono) > 13:
            errores.append("El teléfono debe tener entre 8 y 13 dígitos.")

        if self.rol not in ["cliente", "clinica"]:
            errores.append("El rol es invalido")

        return errores