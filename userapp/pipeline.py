from social_core.exceptions import AuthForbidden
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        print(f'google-oauth2 {response}')
        if 'gender' in response.keys():
            match response['gender']:
                case 'male':
                    user.profile.gender = 'M'
                case 'female':
                    user.profile.gender = 'W'

        if 'tagline' in response.keys():
            user.profile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.about_me = response['aboutMe']

        if 'picture' in response.keys():
            print(response['picture'])
            # user.photo.url = response['picture']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()

    if backend.name == 'vk-oauth2':
        print(f'vk-oauth2 {response}')
        # if 'user_photo' in response.keys():
        #     user.photo.url = response['user_photo']
        user.save()

    if backend.name == 'github-oauth2':
        print(f'github-oauth2 {response}')
        pass
