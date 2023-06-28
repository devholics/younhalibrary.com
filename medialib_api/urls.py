from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'creators', views.CreatorViewSet, basename='creator')
router.register(r'sources', views.MediaSourceViewSet, basename='source')
router.register(r'photos', views.PhotoViewSet, basename='photo')
router.register(r'youtube_videos', views.YouTubeVideoViewSet, basename='youtube_video')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = router.urls
