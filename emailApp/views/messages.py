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
    

    @transaction.atomic
    def post(self, request):
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


    def get(self, request):
        try:
            user_email = request.query_params.get('mail', None)
            # Obtener mensajes where from_user o to_user sea igual al correo proporcionado
            from_messages = MessageFrom.objects.filter(from_user=user_email)
            #to_messages = MessageTo.objects.filter(to_user=user_email)

            # Combinar mensajes de ambas consultas
            #all_messages = from_messages.union(to_messages)

            # Serializar los mensajes
            serialized_messages = []
            for message in from_messages:
                serialized_messages.append({
                    'message_id': message.id,
                    'from_user_name': message.from_user.name,  # Ajusta esto según la estructura de tu modelo de usuario
                    'from_user': message.from_user.email,
                    'to_user': message.from_user.email,
                    'created_at': message.created_at.strftime('%d %b %Y'),  # Formatea la fecha según tus necesidades
                    'subject': message.subject,
                    'body': message.body,
                    'category_id': message.category_id,
                })

            return Response(serialized_messages, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': 'Uncontrolled error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
