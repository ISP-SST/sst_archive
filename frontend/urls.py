from django.urls import path

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
    path('user/login', views.login, name='login'),
    path('access_denied', views.access_denied, name='access_denied'),
]
