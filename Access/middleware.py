from django.utils.functional import SimpleLazyObject
from .acl import Acl


class AclMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.acl = SimpleLazyObject(lambda: Acl(request.user))
        response = self.get_response(request)
        return response
