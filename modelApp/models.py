from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    anio_publicacion = models.PositiveIntegerField()
    categoria = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    cargo = models.CharField(max_length=120)
    fecha_contratacion = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"
