from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from emailApp.serializers.user_serializer import UserSerializer
import bcrypt

class UserCreateView(generics.CreateAPIView):
    """
    Create a new user.
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        Create a new user. If the email already exists, return a 400 status code.
        """
        try:
            # Extract the password from the request
            password = request.data.get('password')

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Replace the plain password with the hashed one in the request data
            request.data['password'] = hashed_password.decode('utf-8')

            serializer = UserSerializer(data=request.data)
            queryset = get_user_model().objects.all()
            if queryset.filter(email=request.data['email']).exists():
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Uncontrolled error:' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class UserCreateView(generics.CreateAPIView):
#     """
#     Create a new user.
#     """
#     serializer_class = UserSerializer

#     def post(self, request):
#         """
#         Create a new user. If the email already exists, return a 400 status code.
#         """
#         try:
#             serializer = UserSerializer(data=request.data)
#             queryset = get_user_model().objects.all()
#             if queryset.filter(email=request.data['email']).exists():
#                 return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'message': 'User created succesfully'}, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'message': 'Uncontrolled error:' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

