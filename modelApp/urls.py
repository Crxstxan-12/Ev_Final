from django.urls import path
from .views import (
    lista_libros,
    detalle_libro,
    pagina_libros,
    pagina_libro_form,
    pagina_libro_detalle,
    lista_trabajadores,
    detalle_trabajador,
    pagina_trabajadores,
    asignar_grupo_usuario,
    mis_permisos,
)


urlpatterns = [
    path('libros/', lista_libros),
    path('libros/<int:pk>/', detalle_libro),
    path('trabajadores/', lista_trabajadores),
    path('trabajadores/<int:pk>/', detalle_trabajador),
    path('usuarios/permisos/asignar/', asignar_grupo_usuario),
    path('usuarios/permisos/mis/', mis_permisos),
    # Páginas HTML
    path('paginas/libros/', pagina_libros),
    path('paginas/libros/nuevo/', pagina_libro_form),
    path('paginas/libros/<int:pk>/', pagina_libro_detalle),
    path('paginas/trabajadores/', pagina_trabajadores),
]
