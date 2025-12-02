from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class LibrosAPITests(APITestCase):
    def setUp(self):
        self.username = 'tester'
        self.password = 'testerpass123'
        User.objects.create_user(username=self.username, password=self.password)

        token_resp = self.client.post('/api/token/', {
            'username': self.username,
            'password': self.password,
        }, format='json')
        self.assertEqual(token_resp.status_code, status.HTTP_200_OK)
        access = token_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_crud_libro(self):
        # Lista inicial
        resp_list = self.client.get('/api/libros/')
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)

        # Crear
        nuevo = {
            'titulo': 'El Quijote',
            'autor': 'Miguel de Cervantes',
            'anio_publicacion': 1605,
            'categoria': 'Novela',
            'disponible': True,
        }
        resp_create = self.client.post('/api/libros/', nuevo, format='json')
        self.assertEqual(resp_create.status_code, status.HTTP_201_CREATED)
        libro_id = resp_create.data['id']

        # Ver detalle
        resp_detail = self.client.get(f'/api/libros/{libro_id}/')
        self.assertEqual(resp_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_detail.data['titulo'], 'El Quijote')

        # Actualizar
        actualizado = {**nuevo, 'titulo': 'El Quijote (Edición Revisada)'}
        resp_update = self.client.put(f'/api/libros/{libro_id}/', actualizado, format='json')
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_update.data['titulo'], 'El Quijote (Edición Revisada)')

        # Eliminar
        resp_delete = self.client.delete(f'/api/libros/{libro_id}/')
        self.assertEqual(resp_delete.status_code, status.HTTP_204_NO_CONTENT)

        # Confirmar 404
        resp_missing = self.client.get(f'/api/libros/{libro_id}/')
        self.assertEqual(resp_missing.status_code, status.HTTP_404_NOT_FOUND)
