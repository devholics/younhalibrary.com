from rest_framework import viewsets

from medialib.models import Creator

from .serializers import CreatorSerializer


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
