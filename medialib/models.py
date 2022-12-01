from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)
    url = models.URLField('URL', blank=True)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=40)
    platform = models.ForeignKey('Platform', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=200, blank=True)
    url = models.URLField('URL', blank=True)

    def __str__(self):
        return self.name + (f' @ {self.platform.name}' if self.platform else '')


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=200, blank=True)

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
        (YOUTUBE, 'Youtube video'),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    url = models.URLField('URL', unique=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey('Creator', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    source_url = models.URLField('Source URL', blank=True)
    verified = models.BooleanField(default=False)   # check if source and creator verified
    display = models.BooleanField(default=True)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    class Meta:
        ordering = ('-created_date',)
        get_latest_by = 'created_date'

    def clean(self):
        if self.type == self.YOUTUBE and not self.url.startswith('https://youtu.be/'):
            raise ValidationError("Youtube URL should start with 'https://youtu.be/'.")

    @property
    def youtube_id(self):
        if self.type != self.YOUTUBE:
            return None
        return self.url[17:]

    def __str__(self):
        return self.title or self.get_type_display() + f" by {self.creator.name if self.creator else 'Unknown'}"
