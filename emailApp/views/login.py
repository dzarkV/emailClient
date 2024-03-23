from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from emailApp.serializers.user_serializer import UserToResponseSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UsersLogin(generics.CreateAPIView):
    """
    Login users.
    """
    serializer_class = UserToResponseSerializer

    def post(self, request):
        """
        Login users and generate JWT tokens for authentication.
        This API endpoint allows users to log in to the application using their email and password.
        Upon successful login, the endpoint generates a refresh token and its corresponding access token 
        as a JSON response. These tokens can be used for further API requests that require authentication.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            

            user = authenticate(request, email=email, password=password)
            
            
            if user is not None:
                # Create JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User successfully logged in',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid email or password'},
                                status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)