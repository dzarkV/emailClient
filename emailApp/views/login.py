from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from emailApp.serializers.user_serializer import UserToResponseSerializer

class UsersLogin(generics.CreateAPIView):
    """
    Login users.
    """
    serializer_class = UserToResponseSerializer

    def post(self, request):
        """
        Users' login, checking if the email and password are in queryset
        """
        try:

            # Get the user from the database
            user = get_user_model().objects.filter(email=request.data['email'], password=request.data['password']).first()

            # If the filter returns an empty queryset, the email or password is invalid
            if user is None:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user_serialized = self.serializer_class(user)
            return Response({'message': 'User successfully logged in', 'data': user_serialized.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': str(e) + ' not provided'}, status=status.HTTP_400_BAD_REQUEST)