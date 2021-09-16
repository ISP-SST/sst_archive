from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.search_view, name='index'),
    path('files/<filename>', views.file_detail, name='file_detail'),
    path('search', views.search_view, name='search'),
    path('toggle-file-selection/<filename>', views.toggle_file_selection,
         name='toggle_file_selection'),
    path('selections/download', views.download_selected_data, name='download_selected_data'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='frontend/account_login.html', redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='frontend/account_logout.html'), name='logout'),
    path('accounts/register/', views.register, name='register'),
]
