from rest_framework import serializers

from medialib.models import Creator, License, Media, MediaSource, Platform, Tag


class CreatorSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Platform.objects.all(),
    )

    class Meta:
        model = Creator
        fields = ['id', 'name', 'platform', 'url', 'description']


class MediaSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaSource
        fields = ['id', 'url', 'title', 'description']


class MediaSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field='url',
        queryset=MediaSource.objects.all(),
    )
    license = serializers.SlugRelatedField(
        slug_field='name',
        queryset=License.objects.all(),
    )

    class Meta:
        model = Media
        fields = ['id', 'type', 'url', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'source',
                  'license', 'verified']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']
