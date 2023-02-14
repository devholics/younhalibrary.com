from django.urls import include, path

from . import views


urlpatterns = [
    path('gallery/', include([
        path('', views.FileMediaListView.as_view(), name='filemedia-list'),
        path('<int:pk>/', views.FileMediaDetailView.as_view(), name='filemedia-detail'),
    ])),
    path('youtube/', include([
        path('', views.YouTubeVideoListView.as_view(), name='youtubevideo-list'),
        path('<int:pk>/', views.YouTubeVideoDetailView.as_view(), name='youtubevideo-detail'),
    ])),
    path('tags/', include([
        path('', views.TagListView.as_view(), name='tag-list'),
        path('<int:pk>/', include([
            path('', views.TagDetailView.as_view(), name='tag-detail'),
            path('gallery/', views.TagGalleryView.as_view(), name='tag-gallery'),
            path('youtube/', views.TagYouTubeView.as_view(), name='tag-youtube'),
        ])),
    ])),
    path('creators/', include([
        path('', views.CreatorListView.as_view(), name='creator-list'),
        path('<int:pk>/', include([
            path('', views.CreatorDetailView.as_view(), name='creator-detail'),
            path('gallery/', views.CreatorGalleryView.as_view(), name='creator-gallery'),
            path('youtube/', views.CreatorYouTubeView.as_view(), name='creator-youtube'),
        ])),
    ])),
    path('license/<int:pk>/', views.license_detail, name='media-license'),
    path('', views.gallery_redirect_view, name='gallery-legacy'),
]
