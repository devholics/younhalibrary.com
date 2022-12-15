from django.contrib import admin
from django.utils.html import format_html

from .models import Creator, ExternalLink, License, Media, MediaSource, Platform, Tag


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform')
    search_fields = ['name']


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url')
    fields = ('name', 'type', 'url', 'description')


class MediaMixin:
    @admin.display(description='Preview')
    def preview(self, obj):
        if obj.type == Media.TYPE_IMAGE:
            return format_html(
                '<img src="{}" alt="{}" height="300">',
                obj.url,
                str(obj)
            )
        elif obj.type == Media.TYPE_VIDEO:
            return format_html(
                '<video src="{}" height="300" controls>Video not supported</video>',
                obj.url
            )
        elif obj.type == Media.TYPE_AUDIO:
            return format_html(
                '<audio src="{}" controls>Audio not supported</audio>',
                obj.url
            )
        elif obj.type == Media.TYPE_YOUTUBE:
            return format_html(
                '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" style="border:0;"></iframe>',
                obj.youtube_id
            )
        else:
            return 'Save to view'


class MediaInline(MediaMixin, admin.StackedInline):
    model = Media
    readonly_fields = ('preview',)
    fields = ('type', 'url', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'verified', 'license', 'display')
    autocomplete_fields = ['creator', 'tags']
    max_num = 30
    show_change_link = True


class MediaSourceAdmin(admin.ModelAdmin):
    fields = ('url', 'title', 'description')
    inlines = [MediaInline]


class MediaAdmin(MediaMixin, admin.ModelAdmin):
    readonly_fields = ('preview',)
    fields = ('type', 'url', 'preview', 'title', 'description', 'creator',
              'date', 'date_exact', 'tags', 'source', 'verified', 'license', 'display')
    list_display = ('__str__', 'date', 'upload_time', 'display')
    autocomplete_fields = ['creator', 'tags']
    ordering = ('-upload_time',)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Platform)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(MediaSource, MediaSourceAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
