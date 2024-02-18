from django.db import models
from .user import User


class MessageTo(models.Model):
    """
    MessageTo model to store the message to the user.
    """

    message_id = models.AutoField(primary_key=True)

    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
