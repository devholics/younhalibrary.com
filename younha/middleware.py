from django.conf import settings


class APIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith('api'):
            request.urlconf = 'younha.urls.api'
        response = self.get_response(request)
        return response
