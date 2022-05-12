from pathlib import Path


def user_photo_directory_path(instance, filename):
    return Path('user_avatars', f'user_{instance.pk}', f'{filename}')
