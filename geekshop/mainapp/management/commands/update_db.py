from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import os
import json

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategory, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            user_profile = ShopUserProfile.objects.create(user=user)
            user_profile.save()


