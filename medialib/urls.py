from django.urls import path

from . import views


urlpatterns = [
    path('', views.MediaListView.as_view(), name='media-list'),
    path('tag/<int:pk>/', views.MediaTagView.as_view(), name='media-tag'),
    path('creator/<int:pk>/', views.MediaCreatorView.as_view(), name='media-creator'),
    path('archive/', views.MediaArchiveIndexView.as_view(), name='media-archive'),
    path('archive/<int:year>/', views.MediaYearArchiveView.as_view(), name='media-year-archive'),
    path('archive/<int:year>/<str:month>/', views.MediaMonthArchiveView.as_view(), name='media-month-archive'),
    path('archive/<int:year>/<str:month>/<int:day>/',
         views.MediaDayArchiveView.as_view(), name='media-day-archive'),
    path('<int:pk>/', views.MediaDetailView.as_view(), name='media-detail'),
    path('search/', views.MediaSearchView.as_view(), name='media-search'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('creators/', views.CreatorListView.as_view(), name='creator-list'),
    path('license/<int:pk>/', views.LicenseView.as_view(), name='media-license'),
]
