from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from articlesapp.models import Articles


class Command(BaseCommand):
    help = 'creates a test set of articles in the database'

    def add_arguments(self, parser):
        parser.add_argument('-q', type=int, default=22,
                            help='number of instances')

    def handle(self, *args, **options):
        Articles.objects.all().delete()
        for _ in range(options['q']):
            mixer.blend(Articles)
        self.stdout.write('done!')
