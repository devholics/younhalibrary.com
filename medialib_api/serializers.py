from rest_framework import serializers

from medialib.models import Creator, CreatorWebsite, License, Photo, YouTubeVideo, MediaSource, Tag, Video


class CreatorWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorWebsite
        fields = ['platform', 'url']


class CreatorSerializer(serializers.ModelSerializer):
    websites = CreatorWebsiteSerializer(many=True, read_only=True)

    class Meta:
        model = Creator
        fields = ['id', 'name', 'websites', 'description']


class MediaSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaSource
        fields = ['id', 'url', 'title', 'description']


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['type', 'name', 'url', 'description', 'display']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


class PhotoSerializer(serializers.ModelSerializer):
    source = MediaSourceSerializer(read_only=True)
    license = LicenseSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'url', 'thumbnail_url', 'width', 'height', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'source',
                  'license']


class PhotoWritableSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field='url',
        queryset=MediaSource.objects.available(),
    )
    license = serializers.SlugRelatedField(
        slug_field='name',
        queryset=License.objects.all(),
        allow_null=True,
        required=False,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        allow_empty=True,
    )

    class Meta:
        model = Photo
        fields = ['id', 'url', 'thumbnail_url', 'width', 'height', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'source',
                  'license']


class VideoSerializer(serializers.ModelSerializer):
    source = MediaSourceSerializer(read_only=True)
    license = LicenseSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'url', 'thumbnail_url', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'source',
                  'license']


class VideoWritableSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field='url',
        queryset=MediaSource.objects.available(),
    )
    license = serializers.SlugRelatedField(
        slug_field='name',
        queryset=License.objects.all(),
        allow_null=True,
        required=False,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        allow_empty=True,
    )

    class Meta:
        model = Video
        fields = ['id', 'url', 'thumbnail_url', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'source',
                  'license']


class YouTubeVideoSerializer(serializers.ModelSerializer):
    license = serializers.SlugRelatedField(
        slug_field='name',
        queryset=License.objects.all(),
        allow_null=True,
        required=False,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        allow_empty=True,
    )

    class Meta:
        model = YouTubeVideo
        fields = ['id', 'youtube_id', 'title', 'description',
                  'creator', 'date', 'date_exact', 'tags', 'license', 'embeddable']
