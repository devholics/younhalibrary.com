import django_filters

from .models import Creator, Photo, Tag, YouTubeVideo


class MediaDateFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    day = django_filters.NumberFilter(field_name='date', lookup_expr='day')


class MediaSearchFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    creator = django_filters.ModelChoiceFilter(
        queryset=Creator.objects.all()
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all()
    )


class PhotoFilter(MediaDateFilter):
    class Meta:
        model = Photo
        fields = ['date']


class YouTubeVideoFilter(MediaDateFilter):
    class Meta:
        model = YouTubeVideo
        fields = ['date']


class PhotoSearchFilter(MediaSearchFilter):
    class Meta:
        model = Photo
        fields = ['date', 'creator', 'tags']


class YouTubeVideoSearchFilter(MediaSearchFilter):
    class Meta:
        model = YouTubeVideo
        fields = ['date', 'creator', 'tags']
