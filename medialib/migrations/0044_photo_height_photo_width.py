# Generated by Django 4.2.2 on 2023-06-28 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0043_alter_audio_options_alter_photo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
