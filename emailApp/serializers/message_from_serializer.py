from rest_framework import serializers
from emailApp.models import MessageFrom


class MessageFromSerializer(serializers.ModelSerializer):
    """
    Serializer for the MessageFrom model, defining the fields to be included in the serialization.
    """
    class Meta:
        model = MessageFrom
        fields = ('id', 'subject', 'body', 'created_at', 'from_user', 'category_id', 'isActive')
        read_only_fields = ('id', 'created_at')
