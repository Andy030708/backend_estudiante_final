import pytest
from rest_framework.test import APIClient
from rest_framework import status
from estudiantes.models import Estudiante


@pytest.fixture
def api_client():
    """Fixture: Cliente API para las pruebas."""
    return APIClient()


@pytest.fixture
def crear_estudiante():
    """Fixture: Función para crear estudiantes de prueba."""

    def _crear_estudiante(**kwargs):
        defaults = {
            "nombre": "Test User",
            "edad": 20,
            "carrera": "Software",
            "promedio": 8.00,
        }
        defaults.update(kwargs)
        return Estudiante.objects.create(**defaults)

    return _crear_estudiante


@pytest.mark.django_db
class TestEstudianteAPI:
    """Pruebas unitarias para los endpoints de la API."""

    # ===== TESTS DE LISTAR =====
    def test_listar_estudiantes_vacio(self, api_client):
        """Test: Listar cuando no hay estudiantes."""
        response = api_client.get("/api/estudiantes/")

        assert response.status_code == status.HTTP_200_OK

    def test_listar_estudiantes_con_datos(self, api_client, crear_estudiante):
        """Test: Listar estudiantes existentes."""
        crear_estudiante(nombre="Juan")
        crear_estudiante(nombre="María")

        response = api_client.get("/api/estudiantes/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    # ===== TESTS DE CREAR =====
    def test_crear_estudiante_exitoso(self, api_client):
        """Test: Crear estudiante con datos válidos."""
        data = {
            "nombre": "Nuevo Estudiante",
            "edad": 22,
            "carrera": "Software",
            "promedio": 8.50,
        }

        response = api_client.post("/api/estudiantes/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["nombre"] == "Nuevo Estudiante"
        assert Estudiante.objects.count() == 1

    def test_crear_estudiante_sin_nombre(self, api_client):
        """Test: Error al crear sin nombre."""
        data = {"edad": 22, "carrera": "Software", "promedio": 8.50}

        response = api_client.post("/api/estudiantes/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "nombre" in response.data

    def test_crear_estudiante_sin_edad(self, api_client):
        """Test: Error al crear sin edad."""
        data = {"nombre": "Test", "carrera": "Software", "promedio": 8.50}

        response = api_client.post("/api/estudiantes/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # ===== TESTS DE OBTENER POR ID =====
    def test_obtener_estudiante_existente(self, api_client, crear_estudiante):
        """Test: Obtener estudiante por ID válido."""
        estudiante = crear_estudiante(nombre="Carlos")

        response = api_client.get(f"/api/estudiantes/{estudiante.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Carlos"

    def test_obtener_estudiante_no_existente(self, api_client):
        """Test: Error 404 al buscar ID inexistente."""
        response = api_client.get("/api/estudiantes/9999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # ===== TESTS DE ACTUALIZAR =====
    def test_actualizar_estudiante_completo(self, api_client, crear_estudiante):
        """Test: Actualización completa (PUT)."""
        estudiante = crear_estudiante(nombre="Original")
        data = {
            "nombre": "Actualizado",
            "edad": 25,
            "carrera": "Redes",
            "promedio": 9.00,
        }

        response = api_client.put(
            f"/api/estudiantes/{estudiante.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Actualizado"

    def test_actualizar_estudiante_parcial(self, api_client, crear_estudiante):
        """Test: Actualización parcial (PATCH)."""
        estudiante = crear_estudiante(nombre="Original", carrera="Software")
        data = {"nombre": "Solo Nombre Cambiado"}

        response = api_client.patch(
            f"/api/estudiantes/{estudiante.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Solo Nombre Cambiado"
        assert response.data["carrera"] == "Software"

    # ===== TESTS DE ELIMINAR =====
    def test_eliminar_estudiante(self, api_client, crear_estudiante):
        """Test: Eliminar estudiante existente."""
        estudiante = crear_estudiante()

        response = api_client.delete(f"/api/estudiantes/{estudiante.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert Estudiante.objects.count() == 0

    def test_eliminar_estudiante_no_existente(self, api_client):
        """Test: Error 404 al eliminar ID inexistente."""
        response = api_client.delete("/api/estudiantes/9999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # ===== TESTS DE FILTRO POR CARRERA =====
    def test_filtrar_por_carrera(self, api_client, crear_estudiante):
        """Test: Filtrar estudiantes por carrera."""
        crear_estudiante(nombre="Juan", carrera="Software")
        crear_estudiante(nombre="María", carrera="Software")
        crear_estudiante(nombre="Pedro", carrera="Redes")

        response = api_client.get("/api/estudiantes/?carrera=Software")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_filtrar_carrera_sin_resultados(self, api_client, crear_estudiante):
        """Test: Filtro sin coincidencias."""
        crear_estudiante(carrera="Software")

        response = api_client.get("/api/estudiantes/?carrera=Medicina")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    # ===== TESTS DE PROMEDIO GENERAL =====
    def test_promedio_general(self, api_client, crear_estudiante):
        """Test: Calcular promedio general."""
        crear_estudiante(promedio=8.00)
        crear_estudiante(promedio=9.00)
        crear_estudiante(promedio=10.00)

        response = api_client.get("/api/estudiantes/promedio-general/")

        assert response.status_code == status.HTTP_200_OK
        assert float(response.data["promedio_general"]) == 9.00
        assert response.data["total_estudiantes"] == 3

    def test_promedio_general_sin_estudiantes(self, api_client):
        """Test: Promedio general sin estudiantes registrados."""
        response = api_client.get("/api/estudiantes/promedio-general/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
