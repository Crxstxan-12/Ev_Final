from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Libro, Trabajador
from .serializers import LibroSerializer, TrabajadorSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def lista_libros(request):
    if request.method == 'GET':
        q = request.GET.get('q', '').strip()
        qs = Libro.objects.all()
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(autor__icontains=q))
        serializer = LibroSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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

def pagina_trabajadores(request):
    return render(request, 'modelApp/trabajadores_list.html')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def asignar_grupo_usuario(request):
    username = request.data.get('username')
    group_name = request.data.get('group', 'EditoresLibros')
    if not username:
        return Response({'detail': 'username requerido'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    group, _ = Group.objects.get_or_create(name=group_name)
    if group_name == 'EditoresLibros':
        codenames = ['view_libro','add_libro','change_libro','delete_libro','view_trabajador']
        perms = list(Permission.objects.filter(codename__in=codenames))
        group.permissions.set(perms)
    user.groups.add(group)
    return Response({
        'user': user.username,
        'groups': list(user.groups.values_list('name', flat=True)),
        'group_permissions': list(group.permissions.values_list('codename', flat=True)),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_permisos(request):
    perms = sorted(list(request.user.get_all_permissions()))
    return Response({'permissions': perms})
