from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.categories import Categories
from emailApp.models.categories_users import CategoriesUser
from emailApp.serializers.categories_serializer import CategoriesSerializer


class CategoryView(APIView):
    """
    API View for handling category-related operations.
    """

    def get(self, request):
        """
        Retrieve categories associated with a given user's email.

        Parameters:
        - email (str): The email of the user to retrieve categories for.

        Returns:
        - Response: JSON response containing categories or an error message.
        """
        try:
            email = request.GET.get('email', None)

            if not User.objects.filter(email=email).exists():
                return Response({'message': 'Invalid email(s)'}, status=status.HTTP_400_BAD_REQUEST)

            if email is None:
                return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user_categories = CategoriesUser.objects.filter(email=email).values_list('category_id', flat=True)
                categories = Categories.objects.filter(category_id__in=user_categories)
            except CategoriesUser.DoesNotExist:
                return Response([], status=status.HTTP_400_BAD_REQUEST)

            serializer = CategoriesSerializer(categories, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self, request):
        """
        Create a new category and associate it with a user.

        Parameters:
        - email (str): The email of the user to associate the category with.
        - Other category-related fields.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            serializer = CategoriesSerializer(data=request.data)

            if serializer.is_valid():

                category_instance = serializer.save()

                user_email = request.data.get('email')
                user_instance = User.objects.get(email=user_email)

                CategoriesUser.objects.create(
                    email=user_instance,
                    category_id=category_instance
                )

                return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
            
            return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
