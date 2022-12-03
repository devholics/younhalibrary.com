from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Creator, ExternalLink, Media, Tag


class MediaViewMixin:
    model = Media
    queryset = Media.objects.filter(display=True)
    date_field = 'created_date'
    paginate_by = settings.MEDIALIB_PAGINATION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag_list = Tag.objects.annotate(num_media=Count('media'))
        context['tag_list'] = tag_list.order_by('-num_media')[:settings.MEDIALIB_TAG_LIMIT]

        creator_list = Creator.objects.annotate(num_media=Count('media'))
        context['creator_list'] = creator_list.order_by('-num_media')[:settings.MEDIALIB_CREATOR_LIMIT]

        context['external_links'] = ExternalLink.objects.all()
        context['display_count'] = self.get_queryset().count()
        return context


class MediaListView(MediaViewMixin, ListView):
    pass


class MediaArchiveIndexView(MediaViewMixin, ArchiveIndexView):
    pass


class MediaYearArchiveView(MediaViewMixin, YearArchiveView):
    make_object_list = True


class MediaMonthArchiveView(MediaViewMixin, MonthArchiveView):
    pass


class MediaDayArchiveView(MediaViewMixin, DayArchiveView):
    pass


class MediaDetailView(MediaViewMixin, DetailView):
    pass


class MediaTagView(MediaViewMixin, ListView):
    template_name = 'medialib/media_tag.html'

    def get_queryset(self):
        return super().get_queryset().filter(tags=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = tag
        return context


class MediaCreatorView(MediaViewMixin, ListView):
    template_name = 'medialib/media_creator.html'

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        creator = get_object_or_404(Creator, pk=self.kwargs['pk'])
        context['creator'] = creator
        return context
