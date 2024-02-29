from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emailApp.models.categories import Categories
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class MessageViewFilter(APIView):
    """
    API View for filtering and managing messages based on category and user email.
    """

    def get(self, request):
        """
        Retrieve messages for a specified user and category.

        Parameters:
        - category_id (int): The ID of the category for filtering messages.
        - email (str): The email of the user to retrieve messages for.

        Returns:
        - Response: JSON response containing filtered messages or an error message.
        """
        try:
            category_id = request.query_params.get('category_id')
            email = request.query_params.get('email', None)

            if category_id is None or email is None:
                return Response({'message': 'Both category_id and email are required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

            category = get_object_or_404(Categories, category_id=category_id)
            
            messages = MessageTo.objects.filter(to_user=email, message_id__category_id=category)

            if not messages.exists():
                return Response({'message': 'No messages for the specified user and category'}, status=status.HTTP_400_BAD_REQUEST)
            
            serialized_messages = []
            for message in messages:
                if message.message_id.isActive == True:
                    serialized_messages.append({
                        'message_id': message.message_id.id,
                        'from_user_name': message.message_id.from_user.name,
                        'from_user': message.message_id.from_user.email,
                        'to_user': message.to_user.email if message.to_user else None,
                        'to_user_name': message.to_user.name if message.to_user else None,
                        'category_name': category.category_name,
                        'created_at': message.message_id.created_at.strftime('%d %b %Y %H:%M'),
                        'subject': message.message_id.subject,
                        'body': message.message_id.body,
                        'category_id': category.category_id,
                    })

            return Response(serialized_messages, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def patch(self, request):
        """
        Deactivate a message by setting its 'isActive' field to False.

        Parameters:
        - message_id (int): The ID of the message to deactivate.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            message_id = request.data.get('message_id')

            if message_id is None:
                return Response({'message':"No message_id provided."}, status=status.HTTP_400_BAD_REQUEST)

            message = get_object_or_404(MessageFrom, id=message_id)
            message.isActive = False
            message.save()

            return Response({'message': 'Message deactivated successfully'}, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response({'message': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)