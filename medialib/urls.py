from django.urls import path

from . import views


urlpatterns = [
    path('', views.MediaListView.as_view(), name='media-list'),
    path('tag/<int:pk>/', views.MediaListView.as_view(), name='media-tag'),
    path('archive/', views.MediaArchiveIndexView.as_view(), name='media-archive'),
    path('archive/<int:year>/', views.MediaYearArchiveView.as_view(), name='media-year-archive'),
    path('archive/<int:year>/<str:month>/', views.MediaMonthArchiveView.as_view(), name='media-month-archive'),
    path('archive/<int:year>/<str:month>/<int:day>/',
         views.MediaDayArchiveView.as_view(), name='media-day-archive')
]
