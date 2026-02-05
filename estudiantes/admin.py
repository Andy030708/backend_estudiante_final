from django.contrib import admin
from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "edad", "carrera", "promedio")
    list_filter = ("carrera",)
    search_fields = ("nombre", "carrera")
