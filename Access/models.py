from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import caches
from django.contrib.auth.models import Group
from django.conf import settings

from Company.models import Company


class AccessGroup(models.Model):
    """
    Per User information about membership in Group per Company
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        db_table = 'access_group'
        unique_together = ('user', 'group', 'company')


class AccessModule(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'access_module'


class AccessPermission(models.Model):
    module = models.ForeignKey(AccessModule, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group)

    class Meta:
        db_table = 'access_permission'
        unique_together = (('module', 'slug'),)

    def __str__(self):
        return f"Permission {self.name}"

    def has_access(self, user, company=None):
        if not user.is_active:
            return False

        if user.is_superuser:
            return True

        qs = AccessGroup.objects.filter(user=user)
        if company:
            qs = qs.filter(company=company)

        user_groups = set(qs.values_list('group', flat=True))
        permission_groups = set(self.groups.all().values_list('id', flat=True))
        return not user_groups.isdisjoint(permission_groups)

    def get_companies(self, user, flat=False):
        qs = AccessGroup.objects.filter(
            user=user,
            group__in=self.groups.all()).distinct()

        if flat:
            return list(qs.values_list('company', flat=True))

        return [ item.company for item in qs ]
