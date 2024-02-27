from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from emailApp.serializers.user_serializer import UserSerializer

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

            # # Check if email is in the request data
            if 'email' not in request.data:
                return Response({'email': ['This field is required']}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize the request data
            serializer = UserSerializer(data=request.data) 

            queryset = get_user_model().objects.all()

            # # Check if the email already exists
            if queryset.filter(email=request.data['email']).exists():
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save the user if the serializer is valid
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

