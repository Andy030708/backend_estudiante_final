from django.db import models


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    carrera = models.CharField(max_length=100)
    promedio = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = "estudiantes"
        ordering = ["id"]

    def __str__(self):
        return f"{self.nombre} - {self.carrera}"
