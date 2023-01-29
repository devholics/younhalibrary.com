# Generated by Django 4.1.4 on 2023-01-10 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0028_mediasource_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creator',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mediasource',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]