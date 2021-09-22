from django.urls import include, path
from rest_framework import routers

from api import views

router_v1 = routers.DefaultRouter()
router_v1.register(r'data_location', views.DataLocationViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/search', views.search_data_locations),
]
