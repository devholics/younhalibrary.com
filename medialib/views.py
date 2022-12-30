from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import MediaSearchForm
from .models import Creator, ExternalLink, License, Media, Tag


class GalleryMixin:
    sidebar_queryset = Media.objects.filter(Q(type=Media.TYPE_YOUTUBE) | Q(license__isnull=False), display=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.sidebar_queryset  # Do not use self.get_queryset()!
        tag_list = Tag.objects.annotate(
            num_media=Count('media', filter=Q(media__in=qs))
        ).filter(num_media__gt=0)
        context['tag_list'] = tag_list.order_by('-num_media')[:settings.MEDIALIB_TAG_LIMIT]

        creator_list = Creator.objects.annotate(
            num_media=Count('media', filter=Q(media__in=qs))
        ).filter(num_media__gt=0)
        context['creator_list'] = creator_list.order_by('-num_media')[:settings.MEDIALIB_CREATOR_LIMIT]
        context['external_links'] = ExternalLink.objects.all()
        return context


class MediaViewMixin:
    queryset = Media.objects.filter(Q(type=Media.TYPE_YOUTUBE) | Q(license__isnull=False), display=True)
    date_field = 'date'
    paginate_by = settings.MEDIALIB_PAGINATION
    media_sort = 'date'
    media_order = 'desc'

    def get_ordering(self):
        sort = self.request.GET.get('sort', self.media_sort)
        order = self.request.GET.get('order', self.media_order)
        prefix = '' if order == 'asc' else '-'
        if sort == 'random':
            return '?'
        elif sort == 'id':
            return prefix + 'id'
        else:
            # Default: date desc
            return prefix + 'date', prefix + 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Query without page and order
        query = self.request.GET.copy()
        query.pop('page', None)
        sort = query.pop('sort', [self.media_sort])[0]
        order = query.pop('order', [self.media_order])[0]
        context['query'] = query.urlencode()

        # Ordering query
        context['sort'] = sort
        context['order'] = order
        context['ordering_query'] = f'sort={sort}&order={order}'

        # YouTube player
        youtube_params = QueryDict(mutable=True)
        youtube_params.update({
            'enablejsapi': 1,
            'controls': 0,
            'cc_load_policy': 1,
            'loop': 1,
            'fs': 0,
            'modestbranding': 1,
            'iv_load_policy': 3,
            'origin': self.request.build_absolute_uri('/')[:-1]
        })
        context['youtube_query'] = youtube_params.urlencode()

        # Pagination
        if context.get('is_paginated'):
            paginator = context['paginator']
            page = context['page_obj']
            context['page_range'] = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        return context


class MediaListView(MediaViewMixin, GalleryMixin, ListView):
    pass


class MediaArchiveIndexView(MediaViewMixin, GalleryMixin, ArchiveIndexView):
    pass


class MediaYearArchiveView(MediaViewMixin, GalleryMixin, YearArchiveView):
    make_object_list = True


class MediaMonthArchiveView(MediaViewMixin, GalleryMixin, MonthArchiveView):
    pass


class MediaDayArchiveView(MediaViewMixin, GalleryMixin, DayArchiveView):
    pass


class MediaDetailView(MediaViewMixin, GalleryMixin, DetailView):
    pass


class MediaTagView(MediaViewMixin, GalleryMixin, ListView):
    template_name = 'medialib/media_tag.html'

    def get_queryset(self):
        return super().get_queryset().filter(tags=self.kwargs['pk']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = tag
        return context


class MediaCreatorView(MediaViewMixin, GalleryMixin, ListView):
    template_name = 'medialib/media_creator.html'

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        creator = get_object_or_404(Creator, pk=self.kwargs['pk'])
        context['creator'] = creator
        return context


class MediaSearchView(MediaViewMixin, GalleryMixin, ListView):
    template_name = 'medialib/media_search.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = MediaSearchForm(self.request.GET)
        context['tag_search_limit'] = settings.MEDIALIB_TAG_SEARCH_LIMIT
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = MediaSearchForm(self.request.GET)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            type = form.cleaned_data['type']
            tags = form.cleaned_data['tags']
            creator = form.cleaned_data['creator']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            filters = {}
            for tag in tags:
                queryset = queryset.filter(tags=tag)
            if type:
                filters['type'] = type
            if creator:
                filters['creator'] = creator
            if start_date:
                filters['date__gte'] = start_date
            if end_date:
                filters['date__lte'] = end_date
            if keyword:
                queryset = queryset.filter(
                    Q(title__icontains=keyword)
                    | Q(description__icontains=keyword)
                    | Q(tags__name__icontains=keyword)
                    | Q(tags__description__icontains=keyword)
                    | Q(creator__name__icontains=keyword),
                    **filters
                ).distinct()
            else:
                queryset = queryset.filter(**filters)
        return queryset


class TagListView(GalleryMixin, ListView):
    model = Tag


class CreatorListView(GalleryMixin, ListView):
    model = Creator


def license_detail(request, pk):
    license = get_object_or_404(License, pk=pk)
    return HttpResponse(license.description, content_type='text/plain')
