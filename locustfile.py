from locust import HttpUser, task, between


class EstudianteUser(HttpUser):
    """Simulación de usuario que interactúa con la API de estudiantes."""

    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre tareas

    def on_start(self):
        """Se ejecuta al iniciar cada usuario simulado."""
        # Crear un estudiante de prueba para las operaciones
        response = self.client.post(
            "/api/estudiantes/",
            json={
                "nombre": "Usuario Test",
                "edad": 22,
                "carrera": "Software",
                "promedio": 8.5,
            },
        )
        if response.status_code == 201:
            self.estudiante_id = response.json().get("id")
        else:
            self.estudiante_id = None

    @task(3)
    def listar_estudiantes(self):
        """Tarea más frecuente: Listar todos los estudiantes."""
        self.client.get("/api/estudiantes/")

    @task(2)
    def filtrar_por_carrera(self):
        """Filtrar estudiantes por carrera."""
        self.client.get("/api/estudiantes/?carrera=Software")

    @task(2)
    def obtener_promedio_general(self):
        """Obtener el promedio general."""
        self.client.get("/api/estudiantes/promedio-general/")

    @task(1)
    def ver_detalle(self):
        """Ver detalle de un estudiante."""
        if self.estudiante_id:
            self.client.get(f"/api/estudiantes/{self.estudiante_id}/")

    @task(1)
    def crear_estudiante(self):
        """Crear un nuevo estudiante."""
        self.client.post(
            "/api/estudiantes/",
            json={
                "nombre": "Nuevo Estudiante",
                "edad": 20,
                "carrera": "Sistemas",
                "promedio": 7.5,
            },
        )

    @task(1)
    def actualizar_estudiante(self):
        """Actualizar un estudiante existente."""
        if self.estudiante_id:
            self.client.put(
                f"/api/estudiantes/{self.estudiante_id}/",
                json={
                    "nombre": "Usuario Actualizado",
                    "edad": 23,
                    "carrera": "Software",
                    "promedio": 9.0,
                },
            )

    @task(1)
    def health_check(self):
        """Verificar estado del sistema."""
        self.client.get("/api/health/")

    @task(1)
    def metricas(self):
        """Obtener métricas del sistema."""
        self.client.get("/api/metricas/")
