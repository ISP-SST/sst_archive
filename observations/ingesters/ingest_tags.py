import urllib.request

from astropy.io import fits

from observations.models import DataCube, Tag


def get_features_vocabulary():
    features_url = 'https://dubshen.astro.su.se/sst_tags/features.txt'
    http_stream = urllib.request.urlopen(features_url)
    features_list = http_stream.read().decode('utf-8')
    return [line.strip() for line in features_list.splitlines() if line]


def get_events_vocabulary():
    events_url = 'https://dubshen.astro.su.se/sst_tags/events.txt'
    http_stream = urllib.request.urlopen(events_url)
    events_list = http_stream.read().decode('utf-8')
    return [line.strip() for line in events_list.splitlines() if line]


def items_in_vocabulary(vocabulary, items):
    casefold_vocabulary = [e.casefold() for e in vocabulary]
    result = []

    for item in items:
        try:
            index = casefold_vocabulary.index(item.casefold())
            result.append(vocabulary[index])
        except:
            pass

    return result


def ingest_tags(fits_header_hdu: fits.Header, data_cube: DataCube, features_vocabulary, events_vocabulary):
    features_str = fits_header_hdu.get('FEATURES', None)
    events_str = fits_header_hdu.get('EVENTS', None)

    features_missing = features_str is None or features_str == 'MISSING'
    events_missing = events_str is None or events_str == 'MISSING'

    features = []
    events = []

    if features_str and not features_missing:
        features_in_cube = features_str.split(',')
        matched_features = items_in_vocabulary(features_vocabulary, features_in_cube)

        features = [Tag.objects.update_or_create(name=feature.strip(), type=Tag.Type.FEATURE)[0] for feature in
                    matched_features]

    data_cube.features_ingested = not features_missing

    if events_str and not events_missing:
        events_in_cube = events_str.split(',')
        matched_events = items_in_vocabulary(events_vocabulary, events_in_cube)

        events = [Tag.objects.update_or_create(name=event.strip(), type=Tag.Type.EVENT)[0] for event in matched_events]

    data_cube.events_ingested = not events_missing

    data_cube.tags.set(features + events)

    data_cube.save()
