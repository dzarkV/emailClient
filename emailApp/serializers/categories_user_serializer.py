from rest_framework import serializers
from emailApp.models import categories_users


class CategoriesUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CategoriesUser model, defining the fields to be included in the serialization.
    """
    class Meta:
        model = categories_users
        fields = ('id', 'email', 'category_id')
        