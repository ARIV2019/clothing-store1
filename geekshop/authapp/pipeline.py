from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
import urllib.request
import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile
import os

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_400_orig')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    if data['photo_400_orig']:
        urllib.request.urlretrieve(
            data['photo_400_orig'],
            os.path.join(settings.MEDIA_ROOT, 'users_avatars', f'{user.pk}.jpg')
        )
        user.avatar = os.path.join('users_avatars', f'{user.pk}.jpg')

    user.save()


