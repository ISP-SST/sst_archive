from django.urls import include, path

from api import views
from api.v1_router import router_v1

router_v1.register(r'data_cube', views.DataCubeViewSet)
router_v1.register(r'tags', views.TagViewSet)

# Import ingestion endpoints in order to add them to the router.
import ingestion.urls

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/search', views.search_data_cubes),
]
