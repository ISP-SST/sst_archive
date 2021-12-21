import warnings

from astropy.utils.exceptions import AstropyWarning

from .test_ingest_data_cube import *
from .test_sync_with_svo import *

# Ignore Astropy warnings during tests.
warnings.simplefilter('ignore', category=AstropyWarning)
