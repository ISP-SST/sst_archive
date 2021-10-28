import datetime

from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Sum
from django.shortcuts import render

from frontend.complex_filters import get_complex_filter
from frontend.forms import SearchForm, get_initial_search_form, persist_search_form
from observations.models import DataCube, Observation


# Compatibility function. Was introduced in Python 3.9, but we're currently only on 3.7.
def removeprefix(self, prefix):
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


def _utc_datetime_from_date(date):
    return datetime.datetime(year=date.year, month=date.month, day=date.day, tzinfo=datetime.timezone.utc)


class SearchResult:
    def __init__(self, observation_pk, oid, filename, instrument, date, size, thumbnail, r0preview, additional_values, cubes_in_observation):
        self.observation_pk = observation_pk
        self.oid = oid
        self.filename = filename
        self.instrument = instrument
        self.date = date
        self.size = size
        self.thumbnail = thumbnail
        self.r0preview = r0preview
        self.additional_values = additional_values
        self.cubes_in_observation = cubes_in_observation


def _create_search_results_from_observation(request, observation, additional_columns):

    cube_count = observation.cubes.count()
    cube = observation.cubes.all()[0]

    if not hasattr(cube, 'metadata') or not cube.metadata:
        return None

    if hasattr(cube, 'previews'):
        thumbnail = cube.previews.thumbnail if cube.previews else None
    else:
        thumbnail = None

    if hasattr(cube, 'spectral_line_data'):
        r0preview = cube.spectral_line_data.data_preview if cube.spectral_line_data else None
    else:
        r0preview = None

    additional_values = [col.get_value(observation) for col in additional_columns]

    return SearchResult(observation.id, cube.oid, cube.filename, cube.instrument.name,
                        cube.metadata.date_beg, observation.total_size, thumbnail, r0preview, additional_values, cube_count)


class Column:
    def __init__(self, name, only_spec):
        self.name = name
        self.only_spec = only_spec

    def get_name(self):
        return self.name

    def get_value(self, observation):
        raise NotImplementedError()

    def get_only_spec(self):
        return self.only_spec


class MetadataColumn(Column):
    def __init__(self, name, value_key):
        super().__init__(name, 'metadata__%s' % value_key)
        self.value_key = value_key

    def get_value(self, observation):
        return list(set([getattr(cube.metadata, self.value_key) for cube in observation.cubes.all()]))


class TagColumn(Column):
    def __init__(self, name):
        super().__init__(name, 'tags')

    def get_value(self, observation):
        return list(set([tag.name for cube in observation.cubes.all() for tag in cube.tags.all()]))


class AdditionalColumns:
    def __init__(self):
        self.additional_columns = []

    def __iter__(self):
        return self.additional_columns.__iter__()

    def add(self, column: Column):
        self.additional_columns.append(column)

    def get_all_names(self):
        return [col.get_name() for col in self.additional_columns if col.get_name() is not None]

    def get_all_only_specs(self):
        return [col.get_only_spec() for col in self.additional_columns if col.get_only_spec() is not None]


def search_view(request):
    form = SearchForm(request.GET)

    if not form.is_valid():
        # TODO(daniel): Handle this error case.
        pass

    if not hasattr(form, 'cleaned_data') or 'start_date' not in form.cleaned_data:
        form = SearchForm(data=get_initial_search_form(request))
        form.full_clean()

    start_date = form.cleaned_data['start_date'] if 'start_date' in form.cleaned_data else None
    end_date = form.cleaned_data['end_date'] if 'end_date' in form.cleaned_data else None

    instrument = form.cleaned_data['instrument'] if 'instrument' in form.cleaned_data else 'all'

    additional_columns = AdditionalColumns()

    spectral_line_ids = None
    if 'spectral_lines' in form.cleaned_data and form.cleaned_data['spectral_lines'] != '':
        spectral_lines = form.cleaned_data['spectral_lines']
        spectral_line_ids = [int(sl) for sl in spectral_lines]

    features = None
    if 'features' in form.cleaned_data and form.cleaned_data['features']:
        features = form.cleaned_data['features']

    persist_search_form(request, form.cleaned_data)

    complete_query = {}

    query = form.cleaned_data['query']
    freeform_query_q = get_complex_filter(query)

    if 'polarimetry' in form.cleaned_data:
        pol = form.cleaned_data['polarimetry']
        if pol == 'polarimetric':
            complete_query['cubes__metadata__naxis4__exact'] = 4
        elif pol == 'nonpolarimetric':
            complete_query['cubes__metadata__naxis4__exact'] = 1

    if start_date:
        complete_query['cubes__metadata__date_beg__gte'] = _utc_datetime_from_date(start_date)
    if end_date:
        complete_query['cubes__metadata__date_end__lte'] = _utc_datetime_from_date(end_date)

    if spectral_line_ids:
        complete_query['cubes__metadata__filter1__in'] = spectral_line_ids
        additional_columns.add(MetadataColumn('Spectral Line', 'filter1'))

    if features:
        complete_query['cubes__tags__name__in'] = features
        additional_columns.add(TagColumn('Features'))

    if instrument and instrument != 'all':
        complete_query['cubes__instrument__name__iexact'] = instrument

    only_fields = ['oid', 'observation_id', 'filename', 'instrument__name', 'metadata__date_beg', 'size', 'previews',
                   'spectral_line_data', *additional_columns.get_all_only_specs()]

    datacube_dataset = DataCube.objects.only(*only_fields).select_related('metadata', 'instrument', 'previews',
                                                                          'spectral_line_data')

    observations = Observation.objects.all()

    observations = observations.filter(freeform_query_q).filter(**complete_query).\
        prefetch_related(Prefetch('cubes', queryset=datacube_dataset)).annotate(total_size=Sum('cubes__size')).distinct()

    results = [_create_search_results_from_observation(request, observation, additional_columns)
               for observation in observations]

    results = list(filter(None, results))

    paginator = Paginator(results, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'search_results': results,
        'paginator': paginator,
        'page_obj': page_obj,
        'additional_column_names': additional_columns.get_all_names(),
    }

    return render(request, 'frontend/search_results.html', context)
