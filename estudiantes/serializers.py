from rest_framework import serializers
from .models import Estudiante


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = "__all__"


class PromedioGeneralSerializer(serializers.Serializer):
    promedio_general = serializers.DecimalField(max_digits=4, decimal_places=2)
    total_estudiantes = serializers.IntegerField()
