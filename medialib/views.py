from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import django_filters

from .forms import MediaSearchForm
from .models import Creator, ExternalLink, License, Media, Tag


class GalleryMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = Media.objects.displayed()
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


class MediaDateFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    day = django_filters.NumberFilter(field_name='date', lookup_expr='day')

    class Meta:
        model = Media
        fields = ['date']


class MediaViewMixin:
    queryset = Media.objects.displayed()
    date_field = 'date'
    paginate_by = settings.MEDIALIB_PAGINATION
    media_sort = 'date'
    media_order = 'desc'

    def get_raw_queryset(self, qs):
        return qs

    def get_dates(self):
        return self.get_raw_queryset(self.queryset).dates(self.date_field, 'day', order='DESC')

    def get_queryset(self):
        qs = self.get_raw_queryset(super().get_queryset())
        return MediaDateFilter(self.request.GET, queryset=qs).qs

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

        context['dates'] = self.get_dates()

        # Query for page, dates, and order
        base_query = self.request.GET.copy()
        base_query.pop('page', None)
        context['query_for_page'] = base_query.urlencode() + ('&' if base_query else '')

        query = base_query.copy()
        sort = query.pop('sort', [self.media_sort])[0]
        order = query.pop('order', [self.media_order])[0]
        context['query_for_ordering'] = query.urlencode() + ('&' if query else '')

        query = base_query.copy()
        year = query.pop('year', [''])[0]
        month = query.pop('month', [''])[0]
        day = query.pop('day', [''])[0]
        context['date_year'] = int(year) if year.isdigit() else 0
        context['date_month'] = int(month) if month.isdigit() else 0
        context['date_day'] = int(day) if day.isdigit() else 0
        context['query_for_dates'] = query.urlencode() + ('&' if query else '')

        # Ordering
        context['sort'] = sort
        context['order'] = order

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


def archive_view(request):
    return redirect('media-list')


class MediaDetailView(MediaViewMixin, GalleryMixin, DetailView):
    pass


class MediaTagView(MediaViewMixin, GalleryMixin, ListView):
    template_name = 'medialib/media_tag.html'

    def get_raw_queryset(self, qs):
        return qs.filter(tags=self.kwargs['pk']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = tag
        return context


class MediaCreatorView(MediaViewMixin, GalleryMixin, ListView):
    template_name = 'medialib/media_creator.html'

    def get_raw_queryset(self, qs):
        return qs.filter(creator=self.kwargs['pk'])

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

    def get_raw_queryset(self, qs):
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
                qs = qs.filter(tags=tag)
            if type:
                filters['type'] = type
            if creator:
                filters['creator'] = creator
            if start_date:
                filters['date__gte'] = start_date
            if end_date:
                filters['date__lte'] = end_date
            if keyword:
                qs = qs.filter(
                    Q(title__icontains=keyword)
                    | Q(description__icontains=keyword)
                    | Q(tags__name__icontains=keyword)
                    | Q(tags__description__icontains=keyword)
                    | Q(creator__name__icontains=keyword),
                    **filters
                ).distinct()
            else:
                qs = qs.filter(**filters)
        return qs


class TagListView(GalleryMixin, ListView):
    model = Tag


class CreatorListView(GalleryMixin, ListView):
    model = Creator


def license_detail(request, pk):
    license = get_object_or_404(License, pk=pk)
    return HttpResponse(license.description, content_type='text/plain')
