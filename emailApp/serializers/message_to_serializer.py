from rest_framework import serializers
from emailApp.models import MessageTo


class MessageToSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTo
        fields = ('to_user',)
