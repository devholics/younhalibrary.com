from rest_framework import viewsets

from medialib.models import Creator, Media, MediaSource

from .serializers import CreatorSerializer, MediaSerializer, MediaSourceSerializer


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(display=True)
    serializer_class = MediaSerializer


class MediaSourceViewSet(viewsets.ModelViewSet):
    queryset = MediaSource.objects.all()
    serializer_class = MediaSourceSerializer
