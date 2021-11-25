from api import router_v1
from ingestion.api import views

router_v1.register(r'ingest', views.DataCubeIngestionViewSet)
