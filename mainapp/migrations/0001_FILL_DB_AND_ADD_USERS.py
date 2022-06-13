from django.db import migrations
import subprocess


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operations.append(migrations.RunPython(self.fill_db))

    @staticmethod
    def fill_db(*args, **kwargs):
        subprocess.call('py manage.py fill_db_users')
        subprocess.call('py manage.py fill_db_articles')
