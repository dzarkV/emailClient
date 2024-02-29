from django.db import models
from .user import User
from .categories import Categories


class MessageFrom(models.Model):
    """
    Message From model to store the message from the user.
    """

    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
