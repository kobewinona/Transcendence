#just for soil to be able go to admin page


class DisableSessionAndCsrfForAPI:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable session for API endpoints
        if request.path.startswith('/api/'):
            request.session = None  # Disable session
        return self.get_response(request)