from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """
    Custom user manager model
    for authentication.
    """

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a user with the given email and password.
        """

        if not email:
            raise ValueError('Users must be email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User checking extrafields to single user in False.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password with necesary extrafields to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    for client authentication.
    """

    # id = models.AutoField(primary_key=True)
    email = models.EmailField('email', primary_key=True, max_length=30)
    password = models.CharField('password', max_length=256)
    name = models.CharField('name', max_length=30)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    is_staff = models.BooleanField('is_staff', default=False)


    objects = UserManager()
    USERNAME_FIELD = 'email'

