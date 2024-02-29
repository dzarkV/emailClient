from rest_framework import serializers
from emailApp.models.categories import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Categories model, defining the fields to be included in the serialization.
    """
    class Meta:
        model = Categories
        fields = ('category_id', 'category_name', 'color')
        read_only_fields = ('category_id', )
        