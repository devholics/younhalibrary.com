from django.urls import include, path


urlpatterns = [
    path('', include('medialib_api.urls')),
]
