# Generated by Django 5.0.7 on 2024-07-23 22:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_remove_stock_watch_stock_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddConstraint(
            model_name='stock',
            constraint=models.UniqueConstraint(fields=('slug',), name='stock_slug'),
        ),
    ]
