from django.db import migrations, models


def move_source(apps, schema_editor):
    Media = apps.get_model('medialib', 'Media')
    for media in Media.objects.all():
        if media.source:
            media.source_url = media.source
            media.save()


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0010_platform_url_alter_media_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='source_url',
            field=models.URLField(blank=True, verbose_name='Source URL'),
        ),
        migrations.RunPython(move_source),
        migrations.RemoveField(
            model_name='media',
            name='source',
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
