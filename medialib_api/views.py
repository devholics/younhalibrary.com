from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters

from medialib.models import Creator, Media, MediaSource, Tag

from . import serializers


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = serializers.CreatorSerializer

    @action(detail=True, methods=['get'])
    def medias(self, request, **kwargs):
        media_set = Media.objects.public().filter(creator=kwargs['pk']).order_by('id')
        serializer = serializers.MediaSerializer(media_set, many=True)
        return Response(serializer.data)


class MediaFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Media
        fields = ['type', 'creator', 'tags', 'date']


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.public()
    serializer_class = serializers.MediaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MediaFilter

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = serializers.MediaSerializer(data=request.data, many=True, max_length=100)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaSourceViewSet(viewsets.ModelViewSet):
    queryset = MediaSource.objects.all()
    serializer_class = serializers.MediaSourceSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    @action(detail=True, methods=['get'])
    def medias(self, request, **kwargs):
        media_set = Media.objects.public().filter(tags=kwargs['pk']).distinct().order_by('id')
        serializer = serializers.MediaSerializer(media_set, many=True)
        return Response(serializer.data)
