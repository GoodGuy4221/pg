from pathlib import Path


def user_photo_directory_path(instance, filename):
    return Path('user_avatars', f'user_{instance.pk}', f'{filename}')


def article_image_directory_path(instance, filename):
    return Path('images_for_articles', f'article_{instance.pk}', f'{filename}')
