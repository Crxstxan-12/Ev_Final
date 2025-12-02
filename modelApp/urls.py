from django.urls import path
from .views import (
    lista_libros,
    detalle_libro,
    pagina_libros,
    pagina_libro_form,
    pagina_libro_detalle,
    pagina_login,
    registrar_usuario,
)


urlpatterns = [
    path('libros/', lista_libros),
    path('libros/<int:pk>/', detalle_libro),
    # Páginas HTML
    path('paginas/libros/', pagina_libros),
    path('paginas/libros/nuevo/', pagina_libro_form),
    path('paginas/libros/<int:pk>/', pagina_libro_detalle),
    path('paginas/login/', pagina_login),
    path('usuarios/registro/', registrar_usuario),
    path('paginas/registro/', lambda request: __import__('django.shortcuts').shortcuts.render(request, 'modelApp/auth_register.html')),
]
