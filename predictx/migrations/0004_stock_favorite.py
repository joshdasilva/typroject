# Generated by Django 2.1.7 on 2019-04-12 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('predictx', '0003_auto_20190310_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]