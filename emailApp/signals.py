# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from emailApp.models.categories import Categories
from emailApp.models.categories_users import CategoriesUser
from django.apps import AppConfig

@receiver(post_migrate)
def create_default_category(sender, **kwargs):
    if Categories.objects.filter(category_id=0).exists():
        return

    default_category = Categories.objects.create(category_id=0, category_name='Inbox', color='#000000')
    print('Default category and relationships created successfully.')

post_migrate.connect(create_default_category, sender=AppConfig)