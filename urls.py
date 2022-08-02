from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from Customer.views import CustomerListView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('dashboard', login_required(
        TemplateView.as_view(template_name='dashboard.html')), name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customers/', CustomerListView.as_view()),
    path('admin/', admin.site.urls),
]
