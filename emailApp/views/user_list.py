from rest_framework import generics
from rest_framework.views import APIView

from emailApp.models.user import User
from rest_framework.response import Response
from rest_framework import status
from emailApp.serializers.user_serializer import UserToResponseSerializer


class UserListView(APIView):
    """
    List all users.
    """
    serializer_class = UserToResponseSerializer

    def get(self, request=None):
        """
        Retrieve users from the database. If an email is provided, retrieve the user with that email. 
        Not found if the user does not exist.
        """
        queryset = User.objects.filter(is_staff=False)
        email_searched = request.query_params.get('email')

        # If the email is provided, retrieve the user with that email
        if email_searched is not None:
            queryset = queryset.filter(email=email_searched, is_superuser=False).first()
            if queryset is None:
                return Response({'message': 'Email user not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.serializer_class(queryset).data, status=status.HTTP_200_OK)
        
        # If the email is not provided, retrieve all the users
        serializer = UserToResponseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
