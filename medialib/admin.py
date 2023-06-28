from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Creator, CreatorWebsite, ExternalLink, License, Photo, Video, Audio,
    MediaSource, Tag, YouTubeVideo
)


class CreatorWebsiteInline(admin.TabularInline):
    model = CreatorWebsite


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'official')
    search_fields = ['name']
    inlines = [
        CreatorWebsiteInline,
    ]


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url', 'display')
    fields = ('name', 'type', 'url', 'description', 'display')


class YouTubeVideoMixin:
    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.youtube_id:
            return format_html(
                '<iframe width="560" height="315" src="{}" style="border:0;"></iframe>',
                obj.get_embed_url()
            )
        else:
            return 'Save to view'


class MediaSourceAdmin(admin.ModelAdmin):
    fields = ('url', 'title', 'description', 'available')
    list_display = ('title', 'available')
    search_fields = ('title',)


class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('url', 'preview', 'width', 'height', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'source', 'license', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags', 'source']
    ordering = ('-upload_time',)

    @admin.display(description='Preview')
    def preview(self, obj):
        url = obj.get_thumbnail_url()
        if url:
            return format_html(
                '<img src="{}" alt="{}" height="300" referrerpolicy="no-referrer">',
                url,
                str(obj)
            )
        else:
            return 'Save to view'


class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('url', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'source', 'license', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags', 'source']
    ordering = ('-upload_time',)

    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.url:
            return format_html(
                '<video src="{}" height="300" controls>Video not supported</video>',
                obj.url
            )
        else:
            return 'Save to view'


class AudioAdmin(admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('url', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'source', 'license', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags', 'source']
    ordering = ('-upload_time',)

    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.url:
            return format_html(
                '<audio src="{}" controls>Audio not supported</audio>',
                obj.url
            )
        else:
            return 'Save to view'


class YouTubeVideoAdmin(YouTubeVideoMixin, admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('youtube_id', 'preview', 'thumbnail_url', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'license', 'embeddable', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'embeddable', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags']
    ordering = ('-upload_time',)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'category')
    list_filter = ('category',)


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Creator, CreatorAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(MediaSource, MediaSourceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
