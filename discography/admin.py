from django.contrib import admin

from .models import Musician, Song, Album


class MusicianAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SongInline(admin.StackedInline):
    model = Song
    ordering = ('track',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date')
    list_filter = ('artist',)
    inlines = [
        SongInline
    ]
    ordering = ('-release_date',)


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album',)
    readonly_fields = ('artist',)
    fields = ('artist', 'album', 'track', 'title', 'lyrics', 'writers')
    search_fields = ['title', 'lyrics']
    ordering = ('title',)

    @admin.display(description='Artist')
    def artist(self, obj):
        return obj.album.artist


admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
