from rest_framework import serializers
from emailApp.models import MessageTo


class MessageToSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTo
        fields = ('id', 'message_id','to_user')
        read_only_fields = ('id',)
