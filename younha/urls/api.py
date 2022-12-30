from django.urls import include, path

from rest_framework import routers

from medialib_api import views


router = routers.DefaultRouter()
router.register(r'creators', views.CreatorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
