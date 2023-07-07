from django.urls import include, path


urlpatterns = [
    path('', include('medialib.api.urls')),
]
