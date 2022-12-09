from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)
    url = models.URLField('URL', max_length=400, blank=True)
    bootstrap_icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=40)
    platform = models.ForeignKey('Platform', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=200, blank=True)
    url = models.URLField('URL', max_length=400, blank=True)

    def __str__(self):
        return self.name + (f' @ {self.platform.name}' if self.platform else '')


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '# ' + self.name


class Media(models.Model):
    TYPE_IMAGE = 'I'
    TYPE_VIDEO = 'V'
    TYPE_AUDIO = 'A'
    TYPE_YOUTUBE = 'Y'

    TYPE_CHOICES = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_AUDIO, 'Audio'),
        (TYPE_YOUTUBE, 'Youtube video'),
    )

    DATE_TYPE_CREATED = 'C'
    DATE_TYPE_ESTIMATE = 'E'
    DATE_TYPE_UPLOADED = 'U'

    DATE_TYPE_CHOICES = (
        (DATE_TYPE_CREATED, 'Created date'),
        (DATE_TYPE_ESTIMATE, 'Created date estimate'),
        (DATE_TYPE_UPLOADED, 'Uploaded date')
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    url = models.URLField('URL', max_length=400, unique=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey('Creator', null=True, blank=True, on_delete=models.CASCADE)
    date_type = models.CharField(max_length=1, choices=DATE_TYPE_CHOICES)
    date = models.DateField()
    tags = models.ManyToManyField('Tag', blank=True)
    source_url = models.URLField('Source URL', max_length=400, blank=True)
    verified = models.BooleanField(default=False)   # check if source and creator verified
    display = models.BooleanField(default=True)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'

    def clean(self):
        if self.type == self.TYPE_YOUTUBE and not self.url.startswith('https://youtu.be/'):
            raise ValidationError("Youtube URL should start with 'https://youtu.be/'.")

    @property
    def youtube_id(self):
        if self.type != self.TYPE_YOUTUBE:
            return None
        return self.url[17:]

    def __str__(self):
        return self.title or self.get_type_display() + f" by {self.creator.name if self.creator else 'Unknown'}"


class ExternalLink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField('URL', max_length=400, unique=True)
    description = models.CharField(max_length=200, blank=True)
    display = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return self.name
