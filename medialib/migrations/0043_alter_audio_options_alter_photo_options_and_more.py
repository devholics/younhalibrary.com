# Generated by Django 4.2.2 on 2023-06-28 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0042_split_media'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audio',
            options={'ordering': ('-date', '-id')},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('-date', '-id')},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ('-date', '-id')},
        ),
        migrations.DeleteModel(
            name='FileMedia',
        ),
    ]
