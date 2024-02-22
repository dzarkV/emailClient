from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from emailApp.serializers.user_serializer import UserToResponseSerializer
import bcrypt

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
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or not password:
                return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the user from the database
            user = get_user_model().objects.filter(email=email).first()

            if user is None:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Now, we'll use bcrypt to compare the hashed password from the database
            # with the hashed password provided during login
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                user_serialized = self.serializer_class(user)
                return Response({'message': 'User successfully logged in', 'data': user_serialized.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)