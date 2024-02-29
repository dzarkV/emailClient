from rest_framework import serializers
from emailApp.models import MessageTo


class MessageToSerializer(serializers.ModelSerializer):
    """
    Serializer for the MessageTo model, defining the fields to be included in the serialization.
    """
    class Meta:
        model = MessageTo
        fields = ('id', 'message_id','to_user')
        read_only_fields = ('id',)
