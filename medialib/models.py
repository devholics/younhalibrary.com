from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.expressions import RawSQL
from django.urls import reverse


class CreatorManager(models.Manager):
    def with_counts(self):
        # An ugly hack to deal with multiple aggregations...
        # https://docs.djangoproject.com/en/4.2/topics/db/aggregation/#combining-multiple-aggregations
        # https://code.djangoproject.com/ticket/10060
        return self.annotate(
            num_photos=RawSQL("SELECT COUNT(*) "
                              "FROM medialib_photo A "
                              "WHERE A.creator_id = medialib_creator.id "
                              "  AND A.public AND A.license_id IS NOT NULL", [], models.IntegerField()),
            num_videos=RawSQL("SELECT COUNT(*) "
                              "FROM medialib_video A "
                              "WHERE A.creator_id = medialib_creator.id "
                              "  AND A.public AND A.license_id IS NOT NULL", [], models.IntegerField()),
            num_youtubevideos=RawSQL("SELECT COUNT(*) "
                                     "FROM medialib_youtubevideo A "
                                     "WHERE A.creator_id = medialib_creator.id "
                                     "  AND A.public AND A.license_id IS NOT NULL", [], models.IntegerField())
        )


class Creator(models.Model):
    name = models.CharField(max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    profile_img_url = models.URLField('Profile image URL', max_length=400, blank=True)
    official = models.BooleanField(default=False)
    public = models.BooleanField(default=True)

    objects = CreatorManager()

    class Meta:
        ordering = ('-official', 'name',)

    def __str__(self):
        return self.name

    def get_profile_img_url(self):
        if not self.profile_img_url:
            from django.templatetags.static import static

            return static('medialib/img/person-fill.svg')
        return self.profile_img_url

    def get_absolute_url(self):
        return reverse('creator-detail', kwargs={'pk': self.pk})

    def get_gallery_url(self):
        return reverse('creator-gallery', kwargs={'pk': self.pk})

    def get_youtube_url(self):
        return reverse('creator-youtube', kwargs={'pk': self.pk})

    def photo_count(self):
        return self.photo_set.displayed().count()

    def video_count(self):
        return self.video_set.displayed().count()

    def gallery_count(self):
        return self.photo_count() + self.video_count()

    def media_count(self):
        return self.gallery_count() + self.youtubevideo_set.displayed().count()


class CreatorWebsite(models.Model):
    PLATFORM_TWITTER = 'TW'
    PLATFORM_YOUTUBE = 'YT'
    PLATFORM_INSTAGRAM = 'IG'
    PLATFORM_NAVER_BLOG = 'NB'
    PLATFORM_TISTORY = 'TI'

    PLATFORM_CHOICES = (
        (PLATFORM_TWITTER, 'Twitter'),
        (PLATFORM_YOUTUBE, 'YouTube'),
        (PLATFORM_INSTAGRAM, 'Instagram'),
        (PLATFORM_NAVER_BLOG, 'Naver Blog'),
        (PLATFORM_TISTORY, 'Tistory'),
    )

    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES, blank=True)
    creator = models.ForeignKey('Creator', related_name='websites', on_delete=models.CASCADE)
    url = models.URLField('URL', max_length=400)
    icon_url = models.URLField('Icon URL', max_length=400, blank=True)

    def get_icon_url(self):
        if not self.icon_url:
            from django.templatetags.static import static

            default_img = 'medialib/img/globe.svg'
            return static(f'medialib/img/{self.platform.lower()}_logo.svg' if self.platform else default_img)
        return self.icon_url


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    category = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('category', 'name')

    def __str__(self):
        return '# ' + self.name

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'pk': self.pk})

    def get_gallery_url(self):
        return reverse('tag-gallery', kwargs={'pk': self.pk})

    def get_youtube_url(self):
        return reverse('tag-youtube', kwargs={'pk': self.pk})

    def photo_count(self):
        return self.photo_set.displayed().count()

    def video_count(self):
        return self.video_set.displayed().count()


class MediaSourceQuerySet(models.QuerySet):
    def available(self):
        return self.filter(available=True)


class MediaSource(models.Model):
    url = models.URLField('URL', max_length=400, unique=True)
    title = models.CharField(max_length=100, blank=True)    # must be official
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    objects = MediaSourceQuerySet.as_manager()

    class Meta:
        ordering = ('-upload_time',)

    def __str__(self):
        return self.title or self.url


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


class MediaQuerySet(models.QuerySet):
    def public(self):
        return self.filter(public=True)

    def displayed(self):
        return self.public().filter(license__isnull=False)


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


class Media(models.Model):
    objects = MediaQuerySet.as_manager()

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE)
    date = models.DateField()
    date_exact = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True)
    public = models.BooleanField(default=True)
    license = models.ForeignKey('License', null=True, blank=True, on_delete=models.SET_NULL)
    upload_time = models.DateTimeField(verbose_name='uploaded time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    class Meta:
        abstract = True


class Photo(Media):
    thumbnail_url = models.URLField('Thumbnail URL', max_length=400, blank=True)
    url = models.URLField('URL', max_length=400, unique=True)
    source = models.ForeignKey('MediaSource', on_delete=models.CASCADE)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('-date', '-id')

    def get_thumbnail_url(self):
        if self.thumbnail_url:
            return self.thumbnail_url
        return self.url

    @property
    def official_title(self):
        return self.title or self.source.title or "(Untitled)"

    def __str__(self):
        return self.title or f"Photo by {self.creator.name}"

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})


class Video(Media):
    thumbnail_url = models.URLField('Thumbnail URL', max_length=400, blank=True)
    url = models.URLField('URL', max_length=400, unique=True)
    source = models.ForeignKey('MediaSource', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date', '-id')

    def get_thumbnail_url(self):
        if self.thumbnail_url:
            return self.thumbnail_url
        return self.url

    def __str__(self):
        return self.title or f"Video by {self.creator.name}"


class Audio(Media):
    url = models.URLField('URL', max_length=400, unique=True)
    source = models.ForeignKey('MediaSource', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date', '-id')

    def __str__(self):
        return self.title or f"Audio by {self.creator.name}"


class YouTubeVideo(Media):
    youtube_id = models.CharField('YouTube ID', max_length=20, unique=True)
    thumbnail_url = models.URLField('Thumbnail URL', max_length=400, blank=True)
    embeddable = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date', '-id')
        verbose_name = 'YouTube video'

    @property
    def url(self):
        return f"https://youtu.be/{self.youtube_id}"

    def get_absolute_url(self):
        return reverse('youtubevideo-detail', kwargs={'pk': self.pk})

    def get_embed_url(self):
        return f'https://www.youtube.com/embed/{self.youtube_id}'

    def get_youtube_thumbnail(self):
        return self.thumbnail_url or f'https://i.ytimg.com/vi/{self.youtube_id}/maxresdefault.jpg'

    def __str__(self):
        return self.title or f"YouTube video by {self.creator.name}"
