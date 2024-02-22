from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo
from emailApp.serializers.message_from_serializer import MessageFromSerializer
from emailApp.serializers.message_to_serializer import MessageToSerializer
from django.db import transaction

class MessageView(APIView):
    """
    API endpoint for handling messages.

    Supports GET to retrieve messages and POST to create new messages.
    """
    def get(self, request):
        """
        Retrieve messages for a specified user.

        :param request: HTTP request object.
        :return: Response containing serialized messages or an error message.
        """
        try:
            user_email = request.query_params.get('mail', None)
            from_messages = MessageFrom.objects.filter(from_user=user_email)
            to_messages = MessageTo.objects.filter(to_user=user_email)

            if not from_messages.exists() and not to_messages.exists():
                return Response({'message': 'No messages for the specified user'}, status=status.HTTP_400_BAD_REQUEST)

            messages_to = []
            for to_message in to_messages:
                message_id = to_message.message_id.id

                corresponding_message = MessageFrom.objects.filter(id=message_id).first()
                if corresponding_message:
                    messages_to.append(corresponding_message)

            all_messages = from_messages | MessageFrom.objects.filter(id__in=[msg.id for msg in messages_to])

            serialized_messages = []
            for message in all_messages:
                serialized_messages.append({
                    'message_id': message.id,
                    'from_user_name': message.from_user.name,  
                    'from_user': message.from_user.email,
                    'to_user':  MessageTo.objects.filter(message_id=message.id).first().to_user.email if MessageTo.objects.filter(message_id=message.id).first() else None,
                    'created_at': message.created_at.strftime('%d %b %Y'), 
                    'subject': message.subject,
                    'body': message.body,
                    'category_id': message.category_id,
                })

            return Response(serialized_messages, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request):
        """
        Create a new message.

        :param request: HTTP request object containing message data.
        :return: Response indicating success or failure.
        """
        try:
            to_user_exists = User.objects.filter(email=request.data['to_user']).exists()
            from_user_exists = User.objects.filter(email=request.data['from_user']).exists()

            if not to_user_exists or not from_user_exists:
                return Response({'message': 'Invalid email(s)'}, status=status.HTTP_400_BAD_REQUEST)

            message_data = {
                'subject': request.data['subject'],
                'body': request.data['body'],
                'from_user': User.objects.get(email=request.data['from_user']),
                'category_id': 0 
            } 

            serializer_from = MessageFromSerializer(data=message_data)

            if serializer_from.is_valid():
                instance_from = serializer_from.save(from_user=User.objects.get(email=request.data['from_user']))
                message_to_data = {
                    'message_id': instance_from.id,  
                    'to_user': User.objects.get(email=request.data['to_user']),
                }
                serializer_to = MessageToSerializer(data=message_to_data)
                if serializer_to.is_valid():
                    serializer_to.save()
                    return Response({'message': 'Message created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Invalid data for MessageTo'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

