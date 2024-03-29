# Generated by Django 4.1.4 on 2023-01-30 00:15

from django.db import migrations


def copy_to_new_models(apps, schema_editor):
    Media = apps.get_model('medialib', 'Media')
    FileMedia = apps.get_model('medialib', 'FileMedia')
    YouTubeVideo = apps.get_model('medialib', 'YouTubeVideo')
    for media in Media.objects.all():
        create_kwargs = {
            'title': media.title,
            'description': media.description,
            'creator': media.creator,
            'date': media.date,
            'date_exact': media.date_exact,
            'public': media.public,
            'license': media.license,
            'upload_time': media.upload_time,
            'update_time': media.update_time,
        }
        if media.type == 'Y':
            create_kwargs['youtube_id'] = media.url[17:]
            yt, _ = YouTubeVideo.objects.update_or_create(**create_kwargs)
            yt.tags.add(*media.tags.all())
        else:
            create_kwargs['type'] = media.type
            create_kwargs['url'] = media.url
            create_kwargs['source'] = media.source
            create_kwargs['verified'] = media.verified
            fm, _ = FileMedia.objects.update_or_create(**create_kwargs)
            fm.tags.add(*media.tags.all())


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0032_remove_creator_url_alter_creatorwebsite_platform_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_to_new_models)
    ]