# Create your tasks here

from celery import shared_task
import requests
import uuid
from django.conf import settings
from pathlib import Path

URL = 'https://thecatapi.com/api/images/get?format=src&type=gif'


@shared_task
def download_cat() -> None:
    response = requests.get(url=URL)
    file_expansion = response.headers.get('Content-Type').split('/')[1]
    file_name = Path(settings.MEDIA_ROOT, 'cats', f'{uuid.uuid4()}.{file_expansion}')

    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
