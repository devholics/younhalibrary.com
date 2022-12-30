from .views import CreatorViewSet, MediaViewSet, MediaSourceViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'creators', CreatorViewSet, basename='creator')
router.register(r'sources', MediaSourceViewSet, basename='source')
router.register(r'medias', MediaViewSet, basename='media')

urlpatterns = router.urls
