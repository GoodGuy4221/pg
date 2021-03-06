# Generated by Django 4.0.4 on 2022-06-15 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articlesapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articleimages',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='articlesapp.articles'),
        ),
    ]
