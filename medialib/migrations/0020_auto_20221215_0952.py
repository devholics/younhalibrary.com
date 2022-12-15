# Generated by Django 4.1.3 on 2022-12-15 00:52

from django.db import migrations


def remove_media_without_source(apps, schema_editor):
    Media = apps.get_model('medialib', 'Media')
    for media in Media.objects.filter(creator__isnull=True):
        media.delete()
    for media in Media.objects.filter(source_url=''):
        media.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0019_alter_creator_url_alter_externallink_url_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_media_without_source)
    ]
