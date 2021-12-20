from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/landing_page.html"), name='landing_page'),
    path('observations/<observation_pk>', views.observation_detail, name='observation_detail'),
    path('search', views.search_view, name='search'),
    path('accounts/profile', views.account_profile, name='account_profile')
]
