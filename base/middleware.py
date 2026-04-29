import logging

logger = logging.getLogger(__name__)
from django.http import JsonResponse


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):
        if request.path.startswith("/api"):
            print("Someone is accessing the API endpoint:", request.path)
            print("Request method:", request.method)
            print("Request body:", request.body)
            

           
        
        response = self.get_response(request)
        return response