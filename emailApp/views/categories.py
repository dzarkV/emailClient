from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.categories import Categories
from emailApp.models.categories_users import CategoriesUser
from emailApp.serializers.categories_serializer import CategoriesSerializer

from django.db import transaction

class CategoryView(APIView):

    def get(self, request):
        # Obtener el parámetro de email de la solicitud
        email = request.GET.get('email', None)

        # Validar que se proporcionó el parámetro email
        if email is None:
            return Response({'error': 'El parámetro email es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener las categorías asociadas al usuario con el email proporcionado
        try:
            user_categories = CategoriesUser.objects.filter(email=email).values_list('category_id', flat=True)
            # Filtrar las categorías en base a las asociadas al usuario
            categories = Categories.objects.filter(category_id__in=user_categories)
        except CategoriesUser.DoesNotExist:
            # Si no se encuentra ninguna categoría asociada al usuario, devolver un arreglo vacío y un código 400
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # Serializar las categorías
        serializer = CategoriesSerializer(categories, many=True)
        
        # Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        # Serializar los datos recibidos en la solicitud
        serializer = CategoriesSerializer(data=request.data)

        # Validar y guardar la nueva categoría si los datos son válidos
        if serializer.is_valid():
            # Guardar la categoría
            category_instance = serializer.save()

            # Obtener el usuario correspondiente
            user_email = request.data.get('email')
            user_instance = User.objects.get(email=user_email)

            # Crear la relación en CategoriesUser
            CategoriesUser.objects.create(
                email=user_instance,
                category_id=category_instance
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Devolver errores si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)