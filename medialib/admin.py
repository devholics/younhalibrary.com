from django.contrib import admin

from .models import Creator, Media, Platform, Tag


admin.site.register(Creator)
admin.site.register(Media)
admin.site.register(Platform)
admin.site.register(Tag)
