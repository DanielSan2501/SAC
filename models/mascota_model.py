class Mascota:

    def __init__(self, id_mascota, nombre, especie, raza, sexo, edad, peso, fecha_nacimiento, estado, id_usuario):

        self.id = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.edad = edad
        self.peso = peso
        self.fecha_nacimiento = fecha_nacimiento
        self.estado = estado
        self.id_usuario = id_usuario

    def validar_datos(self):

        errores = []

        if not self.nombre or not all(c.isalpha() or c.isspace() for c in self.nombre):
            errores.append("El nombre de la mascota es obligatorio y solo puede contener letras y espacios.")

        if not self.especie or not all(c.isalpha() or c.isspace() for c in self.especie):
            errores.append("La especie es obligatoria y solo puede contener letras y espacios.")

        if self.raza and not all(c.isalpha() or c.isspace() for c in self.raza):
            errores.append("La raza solo puede contener letras y espacios.")

        if not self.sexo or not all(c.isalpha() or c.isspace() for c in self.sexo):
            errores.append("El sexo es obligatorio y solo puede contener letras y espacios.")

        if self.edad is not None:
            try:
                if int(self.edad) < 0:
                    errores.append("La edad debe ser un número entero y no puede ser negativa.")
            except ValueError:
                errores.append("La edad debe ser un número entero válido.")

        if not self.peso:
            errores.append("El peso es obligatorio.")
        else:
            try:
                if float(self.peso) <= 0:
                    errores.append("El peso debe ser un número positivo, mayor a cero.")
            except ValueError:
                errores.append("El peso debe ser un número válido.")

        if self.fecha_nacimiento is not None:
            try:
                from datetime import datetime
                datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                errores.append("La fecha de nacimiento debe tener el formato YYYY-MM-DD.")

        return errores