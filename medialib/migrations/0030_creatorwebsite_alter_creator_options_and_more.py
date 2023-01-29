# Generated by Django 4.1.4 on 2023-01-29 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0029_alter_creator_description_alter_media_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatorWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=400, verbose_name='URL')),
                ('icon_url', models.URLField(blank=True, max_length=400, verbose_name='Icon URL')),
            ],
        ),
        migrations.AlterModelOptions(
            name='creator',
            options={'ordering': ('name',)},
        ),
        migrations.RemoveConstraint(
            model_name='creator',
            name='unique_platform_name',
        ),
        migrations.RemoveField(
            model_name='creator',
            name='platform',
        ),
        migrations.AddField(
            model_name='creator',
            name='profile_img_url',
            field=models.URLField(blank=True, max_length=400, verbose_name='Profile image URL'),
        ),
        migrations.DeleteModel(
            name='Platform',
        ),
        migrations.AddField(
            model_name='creatorwebsite',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='websites', to='medialib.creator'),
        ),
    ]