from rest_framework import serializers

from medialib.models import Creator


class CreatorSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Creator
        fields = ['name', 'platform', 'url', 'description']
