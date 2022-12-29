from django.contrib.sitemaps import Sitemap

from .models import Creator, Tag


class MediaCreatorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Creator.objects.all()


class MediaTagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.4

    def items(self):
        return Tag.objects.all()
