import pytest
from estudiantes.serializers import EstudianteSerializer
from estudiantes.models import Estudiante


@pytest.mark.django_db
class TestEstudianteSerializer:
    """Pruebas unitarias para el serializer de Estudiante."""

    def test_serializer_campos_validos(self):
        """Test: Serializer con datos válidos."""
        data = {
            "nombre": "Pedro López",
            "edad": 23,
            "carrera": "Software",
            "promedio": 8.75,
        }

        serializer = EstudianteSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["nombre"] == "Pedro López"

    def test_serializer_nombre_requerido(self):
        """Test: Error cuando falta el nombre."""
        data = {"edad": 23, "carrera": "Software", "promedio": 8.75}

        serializer = EstudianteSerializer(data=data)

        assert not serializer.is_valid()
        assert "nombre" in serializer.errors

    def test_serializer_edad_requerida(self):
        """Test: Error cuando falta la edad."""
        data = {"nombre": "Pedro López", "carrera": "Software", "promedio": 8.75}

        serializer = EstudianteSerializer(data=data)

        assert not serializer.is_valid()
        assert "edad" in serializer.errors

    def test_serializer_serializacion(self):
        """Test: Serialización de un objeto existente."""
        estudiante = Estudiante.objects.create(
            nombre="Laura Díaz", edad=21, carrera="Redes", promedio=9.25
        )

        serializer = EstudianteSerializer(estudiante)

        assert serializer.data["nombre"] == "Laura Díaz"
        assert serializer.data["carrera"] == "Redes"
