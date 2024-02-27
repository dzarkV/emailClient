from django.db import models
from .user import User
from .categories import Categories


class CategoriesUser(models.Model):
    """
    
    """
    id = models.AutoField(primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories,on_delete=models.CASCADE)
