class Servicio:

    def __init__(self,  id_servicio, tipo_servicio, nombre, descripcion, precio, duracion, estado, id_clinica):
    
        self.id = id_servicio
        self.tipo_servicio = tipo_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.duracion = duracion
        self.estado = estado
        self.id_clinica = id_clinica

    def validar_datos(self):

        errores = []

        if not self.tipo_servicio or not all(c.isalpha() or c.isspace() for c in self.tipo_servicio):
            errores.append("El tipo de servicio es obligatorio y solo puede contener letras y espacios.")

        if not self.nombre or not all(c.isalpha() or c.isspace() for c in self.nombre):
            errores.append("El nombre del servicio es obligatorio y solo puede contener letras y espacios.")

        if self.descripcion and len(self.descripcion) > 500:
            errores.append("La descripción no puede superar 500 caracteres.")

        if not self.precio:
            errores.append("El precio es obligatorio.")
        else:
            try:
                if float(self.precio) <= 0:
                    errores.append("El precio debe ser mayor a 0.")
                elif float(self.precio) % 1 != 0:
                    errores.append("El precio debe ser un número entero.")
            except ValueError:
                errores.append("El precio debe ser un número válido.")

        if not self.duracion:
            errores.append("La duración es obligatoria.")
        else:
            try:
                if int(self.duracion) <= 0:
                    errores.append("La duración debe ser mayor a 0.")
            except ValueError:
                errores.append("La duración debe ser un número entero válido.")

        if self.estado not in [0, 1]:
            errores.append("El estado debe ser activo o inactivo.")

        if not self.id_clinica:
            errores.append("El servicio debe estar asociado a una clínica.")

        return errores