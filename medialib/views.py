from django.conf import settings
from django.db.models import Case, Count, F, IntegerField, Q, When
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import django_filters

# from .forms import MediaSearchForm
from .models import Creator, ExternalLink, License, FileMedia, YouTubeVideo, Tag


TAG_ORDER_QUERY = '''
SELECT
    A.*,
    num_filemedia + num_youtubevideo as num_media
FROM
    medialib_tag A
LEFT JOIN
    (
        SELECT
            B.id,
            COUNT(C.filemedia_id)
                FILTER (
                    WHERE
                        C.filemedia_id in (
                            SELECT
                                id
                            FROM
                                medialib_filemedia
                            WHERE
                                public AND license_id IS NOT NULL
                        )
                ) as num_filemedia
        FROM
            medialib_tag B
        LEFT JOIN
            medialib_filemedia_tags C
        ON
            B.id = C.tag_id
        GROUP BY
            B.id
    ) D
ON
    A.id = D.id
LEFT JOIN
    (
        SELECT
            E.id,
            COUNT(F.youtubevideo_id)
                FILTER (
                    WHERE
                        F.youtubevideo_id in (
                            SELECT
                                id
                            FROM
                                medialib_youtubevideo
                            WHERE
                                public AND license_id IS NOT NULL
                        )
                ) as num_youtubevideo
        FROM
            medialib_tag E
        LEFT JOIN
            medialib_youtubevideo_tags F
        ON
            E.id = F.tag_id
        GROUP BY
            E.id
    ) G
ON
    A.id = G.id
WHERE
    num_filemedia + num_youtubevideo > 0
ORDER BY
    num_media DESC
'''

CREATOR_ORDER_QUERY = '''
SELECT
    A.*,
    num_filemedia + num_youtubevideo as num_media
FROM
    medialib_creator A
INNER JOIN
    (
        SELECT
            B.id,
            COUNT(C.id)
                FILTER (
                    WHERE
                        C.public AND C.license_id IS NOT NULL
                ) as num_filemedia
        FROM
            medialib_creator B
        LEFT JOIN
            medialib_filemedia C
        ON
            B.id = C.creator_id
        GROUP BY
            B.id
    ) D
ON
    A.id = D.id
INNER JOIN
    (
        SELECT
            E.id,
            COUNT(F.id)
                FILTER (
                    WHERE
                        F.public AND F.license_id IS NOT NULL
                ) as num_youtubevideo
        FROM
            medialib_creator E
        LEFT JOIN
            medialib_youtubevideo F
        ON
            E.id = F.creator_id
        GROUP BY
            E.id
    ) G
ON
    A.id = G.id
WHERE
    num_filemedia + num_youtubevideo > 0
ORDER BY
    num_media DESC
'''


class ExhibitionMixin:
    tag_limit = settings.MEDIALIB_TAG_LIMIT
    creator_limit = settings.MEDIALIB_CREATOR_LIMIT

    def get_creator_queryset(self):
        return Creator.objects.raw(CREATOR_ORDER_QUERY)[:self.creator_limit]

    def get_tag_queryset(self):
        return Tag.objects.raw(TAG_ORDER_QUERY)[:self.tag_limit]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = self.get_tag_queryset()
        context['creator_list'] = self.get_creator_queryset()
        context['external_links'] = ExternalLink.objects.all()
        return context


class MediaDateFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    day = django_filters.NumberFilter(field_name='date', lookup_expr='day')


class FileMediaFilter(MediaDateFilter):
    class Meta:
        model = FileMedia
        fields = ['date']


class YouTubeVideoFilter(MediaDateFilter):
    class Meta:
        model = YouTubeVideo
        fields = ['date']


class MediaViewMixin:
    date_field = 'date'
    media_sort = 'date'
    media_order = 'desc'

    def get_raw_queryset(self):
        return self.queryset

    def get_dates(self):
        return self.get_raw_queryset().dates(self.date_field, 'day', order='DESC')

    def get_queryset(self):
        qs = self.get_raw_queryset()
        return self.filter(self.request.GET, queryset=qs).qs.order_by(*self.get_ordering())

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


class FileMediaMixin(MediaViewMixin, ExhibitionMixin):
    queryset = FileMedia.objects.displayed()
    filter = FileMediaFilter
    paginate_by = settings.MEDIALIB_GALLERY_PAGINATION

    def get_creator_queryset(self):
        return Creator.objects.annotate(
            num_media=Count('filemedia', filter=Q(filemedia__in=self.queryset)),
        ).filter(num_media__gt=0).order_by('-num_media')[:self.creator_limit]

    def get_tag_queryset(self):
        return Tag.objects.annotate(
            num_media=Count('filemedia', filter=Q(filemedia__in=self.queryset)),
        ).filter(num_media__gt=0).order_by('-num_media')[:self.tag_limit]


class YouTubeVideoMixin(MediaViewMixin, ExhibitionMixin):
    queryset = YouTubeVideo.objects.displayed()
    filter = YouTubeVideoFilter
    paginate_by = settings.MEDIALIB_YOUTUBE_PAGINATION

    def get_creator_queryset(self):
        return Creator.objects.annotate(
            num_media=Count('youtubevideo', filter=Q(youtubevideo__in=self.queryset)),
        ).filter(num_media__gt=0).order_by('-num_media')[:self.creator_limit]

    def get_tag_queryset(self):
        return Tag.objects.annotate(
            num_media=Count('youtubevideo', filter=Q(youtubevideo__in=self.queryset)),
        ).filter(num_media__gt=0).order_by('-num_media')[:self.tag_limit]


class FileMediaListView(FileMediaMixin, ListView):
    pass


class YouTubeVideoListView(YouTubeVideoMixin, ListView):
    pass


class FileMediaDetailView(FileMediaMixin, DetailView):
    pass


class YouTubeVideoDetailView(YouTubeVideoMixin, DetailView):
    pass


class TagMixin:
    def get_raw_queryset(self):
        return self.queryset.filter(tags=self.kwargs['pk']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = tag
        context['gallery_preview'] = tag.filemedia_set.displayed().order_by('-date', '-id')[:4]
        context['youtube_preview'] = tag.youtubevideo_set.displayed().order_by('-date', '-id')[:6]
        return context


class TagDetailView(TagMixin, ExhibitionMixin, DetailView):
    model = Tag


class TagGalleryView(TagMixin, FileMediaMixin, ListView):
    template_name = 'medialib/tag_gallery.html'


class TagYouTubeView(TagMixin, YouTubeVideoMixin, ListView):
    template_name = 'medialib/tag_youtube.html'


class CreatorMixin:
    def get_raw_queryset(self):
        return self.queryset.filter(creator=self.kwargs['pk']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        creator = get_object_or_404(Creator, pk=self.kwargs['pk'])
        context['creator'] = creator
        context['gallery_preview'] = creator.filemedia_set.displayed().order_by('-date', '-id')[:4]
        context['youtube_preview'] = creator.youtubevideo_set.displayed().order_by('-date', '-id')[:6]
        return context


class CreatorDetailView(CreatorMixin, ExhibitionMixin, DetailView):
    model = Creator


class CreatorGalleryView(CreatorMixin, FileMediaMixin, ListView):
    template_name = 'medialib/creator_gallery.html'


class CreatorYouTubeView(CreatorMixin, YouTubeVideoMixin, ListView):
    template_name = 'medialib/creator_youtube.html'


class TagListView(ExhibitionMixin, ListView):
    model = Tag
    queryset = Tag.objects.annotate(
        isempty=Case(
            When(category='', then=1),
            default=0,
            output_field=IntegerField(),
        )
    )
    ordering = ('isempty', 'category', 'name')


class CreatorListView(ExhibitionMixin, ListView):
    model = Creator


def license_detail(request, pk):
    media_license = get_object_or_404(License, pk=pk)
    return HttpResponse(media_license.description, content_type='text/plain')


def gallery_redirect_view(request):
    return redirect('filemedia-list')
