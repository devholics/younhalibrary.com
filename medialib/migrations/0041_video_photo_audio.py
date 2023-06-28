# Generated by Django 4.2.2 on 2023-06-28 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0040_youtubevideo_thumbnail_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('date_exact', models.BooleanField(default=True)),
                ('public', models.BooleanField(default=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('thumbnail_url', models.URLField(blank=True, max_length=400, verbose_name='Thumbnail URL')),
                ('url', models.URLField(max_length=400, unique=True, verbose_name='URL')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.creator')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medialib.license')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.mediasource')),
                ('tags', models.ManyToManyField(blank=True, to='medialib.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('date_exact', models.BooleanField(default=True)),
                ('public', models.BooleanField(default=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('thumbnail_url', models.URLField(blank=True, max_length=400, verbose_name='Thumbnail URL')),
                ('url', models.URLField(max_length=400, unique=True, verbose_name='URL')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.creator')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medialib.license')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.mediasource')),
                ('tags', models.ManyToManyField(blank=True, to='medialib.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('date_exact', models.BooleanField(default=True)),
                ('public', models.BooleanField(default=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('url', models.URLField(max_length=400, unique=True, verbose_name='URL')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.creator')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medialib.license')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialib.mediasource')),
                ('tags', models.ManyToManyField(blank=True, to='medialib.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]