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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from emailApp.views import user_create, user_list, messages, login, categories, messages_filter
...


...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# URL patterns for the mail_app_be project
urlpatterns = [
        path("admin/", admin.site.urls),
    path("users/create", user_create.UserCreateView.as_view(), name="users create"),
    path("users/", user_list.UserListView.as_view(), name="users list"),
    path("users/?email=", user_list.UserListView.as_view(), name="users by email"),
    path("users/login", login.UsersLogin.as_view(), name="users login"),
    path("messages/create", messages.MessageView.as_view(), name="messages create"),
    path("messages/getAll", messages.MessageView.as_view(), name="messages list"),
    path("messages/updateCategory",
         messages.MessageView.as_view(), name="update category"),
    path("messages/filterByCategory",
         messages_filter.MessageViewFilter.as_view(), name="filter by category"),
    path("category/create", categories.CategoryView.as_view(),
         name="categories create"),
    path("category/getAll", categories.CategoryView.as_view(),
         name="categories list"),
    path("messages/delete", messages_filter.MessageViewFilter.as_view(),
         name="delete message"),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    # Swagger URLs

]
urlpatterns += staticfiles_urlpatterns()