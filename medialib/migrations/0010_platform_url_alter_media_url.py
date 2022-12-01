# Generated by Django 4.1.3 on 2022-11-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0009_media_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='media',
            name='url',
            field=models.URLField(unique=True, verbose_name='URL'),
        ),
    ]
