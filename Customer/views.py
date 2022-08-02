from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Customer


class CustomerListView(ListView):
    queryset = Customer.objects.select_related('company').order_by('id')

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(company__in=self.request.acl.get_companies('customer', 'view'))
        return qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.acl.check_raise('customer', 'view')
        return super().dispatch(request, *args, **kwargs)
