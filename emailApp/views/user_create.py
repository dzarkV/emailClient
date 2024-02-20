from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from emailApp.serializers.user_serializer import UserSerializer

class UserCreateView(generics.CreateAPIView):
    """
    Create a new user.
    """

    def post(self, request):
        """
        Create a new user. If the email already exists, return a 400 status code.
        """
        try:
            serializer_class = UserSerializer(data=request.data)
            queryset = get_user_model().objects.all()
            if queryset.filter(email=request.data['email']).exists():
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response({'message': 'User created succesfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Uncontrolled error:' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
