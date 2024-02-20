from rest_framework import serializers
from emailApp.models import MessageFrom


class MessageFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFrom
        fields = ('id', 'subject', 'body', 'created_at', 'from_user', 'category_id')
        read_only_fields = ('id', 'created_at')
