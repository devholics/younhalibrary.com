from django.db.models import Count, F

from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from django_filters import rest_framework as filters

from medialib.models import Creator, Photo, YouTubeVideo, MediaSource, Tag, Video

from . import serializers


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.with_counts().annotate(
        num_media=F('num_photos') + F('num_videos')
    ).order_by('-num_media')
    serializer_class = serializers.CreatorSerializer

    @action(detail=True, methods=['get'])
    def gallery(self, request, **kwargs):
        media_set = Photo.objects.public().filter(creator=kwargs['pk']).order_by('id')
        serializer = serializers.PhotoSerializer(media_set, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def youtube(self, request, **kwargs):
        media_set = YouTubeVideo.objects.public().filter(creator=kwargs['pk']).order_by('id')
        serializer = serializers.YouTubeVideoSerializer(media_set, many=True)
        return Response(serializer.data)


class PhotoFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Photo
        fields = ['creator', 'tags', 'date']


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.public()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = PhotoFilter
    ordering_fields = ('date', 'id')
    search_fields = ('title', 'description', 'tags__name', 'tags__description', 'creator__name',
                     'source__title', 'source__description')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.PhotoSerializer
        return serializers.PhotoWritableSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = serializers.PhotoWritableSerializer(data=request.data, many=True, max_length=100)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Video
        fields = ['creator', 'tags', 'date']


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.public()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = VideoFilter
    ordering_fields = ('date', 'id')
    search_fields = ('title', 'description', 'tags__name', 'tags__description', 'creator__name',
                     'source__title', 'source__description')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.VideoSerializer
        return serializers.VideoWritableSerializer


class YouTubeVideoFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = YouTubeVideo
        fields = ['creator', 'tags', 'date']


class YouTubeVideoViewSet(viewsets.ModelViewSet):
    queryset = YouTubeVideo.objects.public()
    serializer_class = serializers.YouTubeVideoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = YouTubeVideoFilter


class MediaSourceViewSet(viewsets.ModelViewSet):
    queryset = MediaSource.objects.all()
    serializer_class = serializers.MediaSourceSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.annotate(num_photos=Count("photo")).order_by("-num_photos")
    serializer_class = serializers.TagSerializer

    @action(detail=True, methods=['get'])
    def gallery(self, request, **kwargs):
        media_set = Photo.objects.public().filter(tags=kwargs['pk']).distinct().order_by('id')
        serializer = serializers.PhotoSerializer(media_set, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def youtube(self, request, **kwargs):
        media_set = YouTubeVideo.objects.public().filter(tags=kwargs['pk']).distinct().order_by('id')
        serializer = serializers.YouTubeVideoSerializer(media_set, many=True)
        return Response(serializer.data)
