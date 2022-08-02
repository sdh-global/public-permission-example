from django.contrib import admin
from .models import AccessModule, AccessPermission, AccessGroup


class AccessPermissionInline(admin.StackedInline):
    model = AccessPermission


@admin.register(AccessModule)
class AccessModuleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [AccessPermissionInline]


@admin.register(AccessGroup)
class AccessGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'company')
    list_filter = ('user', 'group', 'company')
