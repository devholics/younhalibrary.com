from django.urls import path

from . import views


urlpatterns = [
    path('', views.MediaListView.as_view(), name='media-list'),
    path('tag/<int:pk>/', views.MediaTagView.as_view(), name='media-tag'),
    path('creator/<int:pk>/', views.MediaCreatorView.as_view(), name='media-creator'),
    path('archive/', views.archive_view, name='media-archive'),
    path('<int:pk>/', views.MediaDetailView.as_view(), name='media-detail'),
    path('search/', views.MediaSearchView.as_view(), name='media-search'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('creators/', views.CreatorListView.as_view(), name='creator-list'),
    path('license/<int:pk>/', views.license_detail, name='media-license'),
]
