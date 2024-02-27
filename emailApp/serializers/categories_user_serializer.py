from rest_framework import serializers
from emailApp.models import categories_users


class CategoriesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = categories_users
        fields = ('id', 'email', 'category_id')
        