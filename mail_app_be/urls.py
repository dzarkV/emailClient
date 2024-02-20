"""
URL configuration for mail_app_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from emailApp.views import user_create, user_list, messages


# URL patterns for the mail_app_be project
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/create", user_create.UserCreateView.as_view(), name="users create"),
    path("users/", user_list.UserListView.as_view(), name="users list"),
    path("users/?email=", user_list.UserListView.as_view(), name="users by email"),
    path("messages/create", messages.MessageView.as_view(), name="messages create"),
    path("messages/getAll", messages.MessageView.as_view(), name="messages list"),
]

