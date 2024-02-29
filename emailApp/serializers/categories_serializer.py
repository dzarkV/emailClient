from rest_framework import serializers
from emailApp.models.categories import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category_id', 'category_name', 'color')
        read_only_fields = ('category_id', )
        