from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet, metricas

router = DefaultRouter()
router.register(r"estudiantes", EstudianteViewSet, basename="estudiante")

urlpatterns = [
    path("", include(router.urls)),
    path("metricas/", metricas, name="metricas"),
]
