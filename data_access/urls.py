from django.urls import path

from . import views

urlpatterns = [
	path('datasets/<dataset>/download/<oid>', views.download_data_cube, name='download_data_cube'),
]
