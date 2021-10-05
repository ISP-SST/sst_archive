from api import router_v1
from ingestion import views

router_v1.register(r'ingest', views.DataCubeIngestionViewSet)
