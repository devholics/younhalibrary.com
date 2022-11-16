from django.conf import settings
from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=40)
    platform = models.ForeignKey('Platform', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    reference = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    IMAGE = 'I'
    VIDEO = 'V'
    AUDIO = 'A'
    YOUTUBE = 'Y'

    TYPE_CHOICES = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (YOUTUBE, 'Youtube'),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE)
    created_date = models.DateField(null=True, blank=True)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title or self.type
