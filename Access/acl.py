from typing import List
from Company.models import Company

from .models import AccessPermission
from .exceptions import AclDenied


class Acl:
    ATTR_PREFIX = 'has_'

    def __init__(self, user):
        self.user = user

    def __getattr__(self, key):
        if key.startswith(self.ATTR_PREFIX):
            return self.check_acl(key[len(self.ATTR_PREFIX):])
        raise AttributeError(key)

    def __str__(self):
        return '<Acl id: %s>' % self.id

    def check_acl(self, key):
        if not self.user.is_active:
            return False
        args = key.split('_')
        if len(args) < 2:
            raise AttributeError
        return self.check(args[0], '_'.join(args[1:]))

    def check(self, module_slug, permission_slug, company=None) -> bool:
        permission = self.get_permission(module_slug, permission_slug)
        return permission.has_access(self.user, company)

    def get_companies(self, module_slug, permission_slug) -> List[Company]:
        """
        Return allowed list of Companies for requested permission
        """
        if self.user.is_superuser:
            return list(Company.objects.all())

        module = self.get_permission(module_slug, permission_slug)
        return module.get_companies(self.user)

    def get_permission(self, module_slug, permission_slug) -> AccessPermission:
        try:
            return AccessPermission.objects.get(
                    module__slug=module_slug,
                    slug=permission_slug)

        except AccessPermission.DoesNotExist:
            return AccessPermission()

    def check_raise(self, module_slug, permission_slug, company=None):
        if not self.check(module_slug, permission_slug, company):
            module = self.get_permission(module_slug, permission_slug)
            if not module.pk:
                msg = f'permission ({module_slug}:{permission_slug}) was not properly defined'
            else:
                msg = f'Access denied for {module_slug}:{permission_slug}'
            extra = {'module_slug': module_slug,
                     'permission_slug': permission_slug}
            if company:
                extra['company_id'] = company.id

            raise AclDenied(msg, **extra)
