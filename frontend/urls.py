from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_view, name='index'),
    path('files/<filename>', views.data_cube_detail, name='data_cube_detail'),
    path('observations/<observation_pk>', views.observation_detail, name='observation_detail'),
    path('search', views.search_view, name='search'),
    path('accounts/profile', views.account_profile, name='account_profile')
]
