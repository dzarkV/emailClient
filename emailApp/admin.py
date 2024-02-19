from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.message_from import MessageFrom
from .models.message_to import MessageTo

user = get_user_model()
admin.site.register(user)
admin.site.register(MessageFrom)
admin.site.register(MessageTo)
