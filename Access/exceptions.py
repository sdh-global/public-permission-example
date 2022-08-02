from django.core.exceptions import PermissionDenied


class AclDenied(PermissionDenied):
    def __init__(self, msg, **extra):
        self.message = msg
        self.detail = {'message': msg}
        self.detail.update(**extra)
