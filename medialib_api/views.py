from rest_framework import generics, viewsets

from django_filters import rest_framework as filters

from medialib.models import Creator, Media, MediaSource, Tag

from . import serializers


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = serializers.CreatorSerializer


class MediaFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Media
        fields = ['type', 'creator', 'tags', 'date']


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(display=True)
    serializer_class = serializers.MediaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MediaFilter


class MediaSourceViewSet(viewsets.ModelViewSet):
    queryset = MediaSource.objects.all()
    serializer_class = serializers.MediaSourceSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class MediaCreatorAPIView(generics.ListAPIView):
    queryset = Media.objects.filter(display=True)
    serializer_class = serializers.MediaSerializer

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.kwargs['pk']).order_by('id')


class MediaTagAPIView(generics.ListAPIView):
    queryset = Media.objects.filter(display=True)
    serializer_class = serializers.MediaSerializer

    def get_queryset(self):
        return super().get_queryset().filter(tags=self.kwargs['pk']).distinct().order_by('id')
