import pytest
from estudiantes.models import Estudiante


@pytest.mark.django_db
class TestEstudianteModel:
    """Pruebas unitarias para el modelo Estudiante."""

    def test_crear_estudiante(self):
        """Test: Crear un estudiante correctamente."""
        estudiante = Estudiante.objects.create(
            nombre="Juan Pérez", edad=22, carrera="Software", promedio=8.50
        )

        assert estudiante.id is not None
        assert estudiante.nombre == "Juan Pérez"
        assert estudiante.edad == 22
        assert estudiante.carrera == "Software"
        assert float(estudiante.promedio) == 8.50

    def test_str_estudiante(self):
        """Test: Representación string del estudiante."""
        estudiante = Estudiante.objects.create(
            nombre="María García", edad=20, carrera="Sistemas", promedio=9.00
        )

        assert str(estudiante) == "María García - Sistemas"

    def test_ordenamiento_por_id(self):
        """Test: Los estudiantes se ordenan por ID."""
        est1 = Estudiante.objects.create(
            nombre="Carlos", edad=21, carrera="Software", promedio=7.50
        )
        est2 = Estudiante.objects.create(
            nombre="Ana", edad=22, carrera="Sistemas", promedio=8.00
        )

        estudiantes = list(Estudiante.objects.all())

        assert estudiantes[0].id < estudiantes[1].id
