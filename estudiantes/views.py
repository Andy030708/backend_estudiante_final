from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Estudiante
from .serializers import EstudianteSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Estudiantes.

    Endpoints:
    - GET /api/estudiantes/ - Listar todos (con filtro opcional por carrera)
    - POST /api/estudiantes/ - Crear nuevo
    - GET /api/estudiantes/{id}/ - Obtener por ID
    - PUT /api/estudiantes/{id}/ - Actualizar completo
    - PATCH /api/estudiantes/{id}/ - Actualizar parcial
    - DELETE /api/estudiantes/{id}/ - Eliminar
    - GET /api/estudiantes/promedio-general/ - Calcular promedio general
    """

    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        """Permite filtrar por carrera usando query params."""
        queryset = Estudiante.objects.all()
        carrera = self.request.query_params.get("carrera", None)

        if carrera is not None:
            queryset = queryset.filter(carrera__icontains=carrera)

        return queryset

    def create(self, request, *args, **kwargs):
        """Crear estudiante con validación."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Actualizar estudiante."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Eliminar estudiante."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Estudiante eliminado correctamente"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"], url_path="promedio-general")
    def promedio_general(self, request):
        """Endpoint adicional: Calcular promedio general de todos los estudiantes."""
        resultado = Estudiante.objects.aggregate(promedio=Avg("promedio"))
        total = Estudiante.objects.count()

        if total == 0:
            return Response(
                {"message": "No hay estudiantes registrados"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = {
            "promedio_general": round(resultado["promedio"], 2),
            "total_estudiantes": total,
        }

        return Response(data, status=status.HTTP_200_OK)
