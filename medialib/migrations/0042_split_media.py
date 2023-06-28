from django.db import migrations


def copy_to_new_models(apps, schema_editor):
    FileMedia = apps.get_model('medialib', 'FileMedia')
    Photo = apps.get_model('medialib', 'Photo')
    Video = apps.get_model('medialib', 'Video')
    Audio = apps.get_model('medialib', 'Audio')
    photo_objs = []
    video_objs = []
    audio_objs = []
    photo_tag_objs = []
    video_tag_objs = []
    audio_tag_objs = []
    for media in FileMedia.objects.all():
        create_kwargs = {
            'id': media.id,
            'title': media.title,
            'description': media.description,
            'creator': media.creator,
            'date': media.date,
            'date_exact': media.date_exact,
            'public': media.public,
            'license': media.license,
            'upload_time': media.upload_time,
            'update_time': media.update_time,
            'url': media.url,
            'source': media.source,
        }
        if media.type == 'I':
            create_kwargs['thumbnail_url'] = media.thumbnail_url
            photo_objs.append(Photo(**create_kwargs))
            photo_tag_objs.extend([Photo.tags.through(photo_id=media.id, tag_id=tag.id) for tag in media.tags.all()])
        elif media.type == 'V':
            create_kwargs['thumbnail_url'] = media.thumbnail_url
            video_objs.append(Video(**create_kwargs))
            video_tag_objs.extend([Video.tags.through(video_id=media.id, tag_id=tag.id) for tag in media.tags.all()])
        else:
            audio_objs.append(Audio(**create_kwargs))
            audio_tag_objs.extend([Audio.tags.through(audio_id=media.id, tag_id=tag.id) for tag in media.tags.all()])
    Photo.objects.bulk_create(photo_objs)
    Video.objects.bulk_create(video_objs)
    Audio.objects.bulk_create(audio_objs)
    Photo.tags.through.objects.bulk_create(photo_tag_objs)
    Video.tags.through.objects.bulk_create(video_tag_objs)
    Audio.tags.through.objects.bulk_create(audio_tag_objs)


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0041_video_photo_audio'),
    ]

    operations = [
        migrations.RunPython(copy_to_new_models)
    ]
