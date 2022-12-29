from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


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
        return self.name + (f' @{self.platform.name}' if self.platform else '')

    def get_absolute_url(self):
        return reverse('media-creator', kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '# ' + self.name

    def get_absolute_url(self):
        return reverse('media-tag', kwargs={'pk': self.pk})


class MediaSource(models.Model):
    url = models.URLField('URL', max_length=400, unique=True)
    title = models.CharField(max_length=100, blank=True)    # must be official
    description = models.CharField(max_length=1000, blank=True)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    def __str__(self):
        return self.title or '(Untitled)'


class License(models.Model):
    TYPE_CREATIVE_COMMONS = 'CC'
    TYPE_OTHERS = 'OT'

    TYPE_CHOICES = (
        (TYPE_CREATIVE_COMMONS, 'Creative Commons License'),
        (TYPE_OTHERS, 'Others')
    )

    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    name = models.CharField(max_length=20, unique=True)
    url = models.URLField('URL', blank=True)
    description = models.TextField(blank=True)
    display = models.BooleanField(default=True)

    def clean(self):
        if not self.url and not self.description:
            raise ValidationError('At least one of URL or description should be provided')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('media-license', kwargs={'pk': self.pk})


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

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    url = models.URLField('URL', max_length=400, unique=True)
    title = models.CharField(max_length=100, blank=True)    # must be official
    description = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE)
    date = models.DateField()
    date_exact = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True)
    source = models.ForeignKey('MediaSource', on_delete=models.CASCADE)
    license = models.ForeignKey('License', null=True, blank=True, on_delete=models.SET_NULL)
    display = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)   # check if source and creator verified
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    def clean(self):
        if self.type == self.TYPE_YOUTUBE and not self.url.startswith('https://youtu.be/'):
            raise ValidationError("Youtube URL should start with 'https://youtu.be/'.")

    @property
    def youtube_id(self):
        if self.type != self.TYPE_YOUTUBE:
            return None
        return self.url[17:]

    @property
    def official_title(self):
        return self.title or self.source.title or self.source.url

    def __str__(self):
        return self.title or (self.get_type_display() + f" by {self.creator.name if self.creator else 'Unknown'}")

    def get_absolute_url(self):
        return reverse('media-detail', kwargs={'pk': self.pk})


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
