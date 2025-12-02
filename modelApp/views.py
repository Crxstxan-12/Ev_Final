from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Libro, Trabajador
from .serializers import LibroSerializer, TrabajadorSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_libros(request):
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def detalle_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({'detail': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_trabajadores(request):
    if request.method == 'GET':
        trabajadores = Trabajador.objects.all()
        serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def detalle_trabajador(request, pk):
    try:
        trabajador = Trabajador.objects.get(pk=pk)
    except Trabajador.DoesNotExist:
        return Response({'detail': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrabajadorSerializer(trabajador)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = TrabajadorSerializer(trabajador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        trabajador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def pagina_libros(request):
    return render(request, 'modelApp/libros_list.html')

def pagina_libro_form(request):
    return render(request, 'modelApp/libro_form.html')

def pagina_libro_detalle(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'modelApp/libro_detail.html', {'libro': libro})

def pagina_login(request):
    return render(request, 'modelApp/auth_login.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password:
        return Response({'detail': 'username y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email or '')
    return Response({'id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
