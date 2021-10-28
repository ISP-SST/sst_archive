from django.urls import path

from . import views

urlpatterns = [
	path('download/<filename>', views.download_data_cube, name='download_data_cube'),
	path('download-multiple', views.download_multiple_data_cubes, name='download_multiple_data_cubes')
]
