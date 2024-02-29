from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, including fields for email, password, and name.
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name',)

class UserToResponseSerializer(UserSerializer):
    """
    Serializer for responding with User information, excluding the password field.
    Extends the UserSerializer class.
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'name',)
        
