from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Creator, CreatorWebsite, ExternalLink, License, FileMedia,
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


class FileMediaMixin:
    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.type == FileMedia.TYPE_IMAGE:
            return format_html(
                '<img src="{}" alt="{}" height="300">',
                obj.url,
                str(obj)
            )
        elif obj.type == FileMedia.TYPE_VIDEO:
            return format_html(
                '<video src="{}" height="300" controls>Video not supported</video>',
                obj.url
            )
        elif obj.type == FileMedia.TYPE_AUDIO:
            return format_html(
                '<audio src="{}" controls>Audio not supported</audio>',
                obj.url
            )
        else:
            return 'Save to view'


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


class FileMediaAdmin(FileMediaMixin, admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('type', 'url', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'source', 'verified', 'license', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags', 'source']
    ordering = ('-upload_time',)


class YouTubeVideoAdmin(YouTubeVideoMixin, admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('youtube_id', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'license', 'public')
    list_display = ('__str__', 'date', 'upload_time', 'public')
    list_filter = ('creator',)
    autocomplete_fields = ['creator', 'tags']
    ordering = ('-upload_time',)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Creator, CreatorAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(MediaSource, MediaSourceAdmin)
admin.site.register(FileMedia, FileMediaAdmin)
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
