from django.db import models
from .message_to import MessageTo


class MessageFrom(models.Model):
    """
    Message From model to store the message from the user.
    """

    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    from_user = models.ForeignKey(MessageTo, on_delete=models.CASCADE)
    category_id = models.IntegerField(default=0)
