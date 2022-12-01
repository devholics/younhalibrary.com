from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic.list import ListView

from .models import Media


class MediaViewMixin:
    queryset = Media.objects.filter(display=True)
    date_field = 'created_date'
    paginate_by = 12


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
