from django.db import models


class Categories(models.Model):
    """
    Categories
    """

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)
    color = models.TextField(max_length=200)
