from django.contrib import admin
from django.utils.html import format_html

from .models import Creator, ExternalLink, Media, Platform, Tag


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform')
    search_fields = ['name']


class MediaAdmin(admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('type', 'url', 'preview', 'title', 'description', 'creator',
              'created_date', 'tags', 'source_url', 'verified', 'display')
    list_display = ('__str__', 'created_date', 'upload_time', 'display')
    autocomplete_fields = ['creator', 'tags']
    ordering = ('-upload_time',)

    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.type == Media.IMAGE:
            return format_html(
                '<img src="{}" alt="{}" height="300">',
                obj.url,
                str(obj)
            )
        elif obj.type == Media.VIDEO:
            return format_html(
                '<video src="{}" height="300" controls>Video not supported</video>',
                obj.url
            )
        elif obj.type == Media.AUDIO:
            return format_html(
                '<audio src="{}" controls>Audio not supported</audio>',
                obj.url
            )
        elif obj.type == Media.YOUTUBE:
            return format_html(
                '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" style="border:0;"></iframe>',
                obj.youtube_id
            )
        else:
            return 'Save to view'


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Platform)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
