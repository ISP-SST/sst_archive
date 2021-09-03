from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('datasets/', views.DatasetListView.as_view(), name='dataset_list'),
    path('', views.DatasetListView.as_view(), name='index'),
    path('datasets/<dataset>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<dataset>/metadata/<oid>/', views.metadata_detail, name='metadata_detail'),
    path('search', views.search_view, name='search'),
    path('toggle-metadata-selection/<dataset>/<oid>', views.toggle_metadata_selection,
         name='toggle_metadata_selection'),
    path('selections/download', views.download_selected_data, name='download_selected_data'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='frontend/account_login.html', redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='frontend/account_logout.html'), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('access_denied', views.access_denied, name='access_denied'),
]
