# Generated by Django 4.1.3 on 2022-12-16 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0023_remove_media_source_url_alter_media_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='display',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='mediasource',
            name='url',
            field=models.URLField(max_length=400, unique=True, verbose_name='URL'),
        ),
    ]