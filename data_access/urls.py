from django.urls import path

from . import views

urlpatterns = [
	path('download/<filename>', views.download_data_cube, name='download_data_cube'),
]
