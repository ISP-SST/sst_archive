from astropy.io import fits

from observations.models import DataCube, Tag


def ingest_tags(fits_header_hdu: fits.Header, data_cube: DataCube):
    # TODO(daniel): This is just a PoC right now. Design needs to be validated, and implementation tested.

    features_str = fits_header_hdu.get('FEATURES', None)
    events_str = fits_header_hdu.get('EVENTS', None)

    tag_collection = []

    if features_str:
        features = [Tag(name=feature.strip()) for feature in features_str.split(',')]
        tag_collection += features

    if events_str:
        events = [Tag(name=event.strip()) for event in events_str.split(',')]
        tag_collection += events

    data_cube.tags.set(tag_collection)
