from django.db import models
from .user import User
from .message_from import MessageFrom

class MessageTo(models.Model):
    """
    MessageTo model to store the message to the user.
    """

    id = models.AutoField(primary_key=True)

    message_id = models.ForeignKey(MessageFrom, on_delete=models.CASCADE)

    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    