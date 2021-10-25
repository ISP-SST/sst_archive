import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

from frontend.complex_filters import get_complex_filter
from frontend.file_selection import is_selected_in_session
from frontend.forms import SearchForm, get_initial_search_form, persist_search_form
from observations.models import DataCube


# Compatibility function. Was introduced in Python 3.9, but we're currently only on 3.7.
def removeprefix(self, prefix):
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


def _utc_datetime_from_date(date):
    return datetime.datetime(year=date.year, month=date.month, day=date.day, tzinfo=datetime.timezone.utc)


class SearchResult:
    def __init__(self, oid, filename, instrument, date, file_size, thumbnail, r0preview, additional_values,
                 selected=False):
        self.oid = oid
        self.filename = filename
        self.instrument = instrument
        self.date = date
        self.file_size = file_size
        self.thumbnail = thumbnail
        self.r0preview = r0preview
        self.selected = selected
        self.additional_values = additional_values


def _create_search_result_from_metadata(request, cube, additional_columns):
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

    additional_values = [col.get_value(cube) for col in additional_columns]

    return SearchResult(cube.oid, cube.filename, cube.instrument.name,
                        cube.metadata.date_beg, cube.size, thumbnail, r0preview, additional_values,
                        is_selected_in_session(request, cube.filename))


class Column:
    def __init__(self, name, only_spec):
        self.name = name
        self.only_spec = only_spec

    def get_name(self):
        return self.name

    def get_value(self, data_cube):
        raise NotImplementedError()

    def get_only_spec(self):
        return self.only_spec


class MetadataColumn(Column):
    def __init__(self, name, value_key):
        super().__init__(name, 'metadata__%s' % value_key)
        self.value_key = value_key

    def get_value(self, data_cube):
        return getattr(data_cube.metadata, self.value_key)


class TagColumn(Column):
    def __init__(self, name):
        super().__init__(name, 'tags')

    def get_value(self, data_cube):
        return [tag.name for tag in data_cube.tags.all()]


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
            complete_query['metadata__naxis4__exact'] = 4
        elif pol == 'nonpolarimetric':
            complete_query['metadata__naxis4__exact'] = 1

    if start_date:
        complete_query['metadata__date_beg__gte'] = _utc_datetime_from_date(start_date)
    if end_date:
        complete_query['metadata__date_end__lte'] = _utc_datetime_from_date(end_date)

    if spectral_line_ids:
        complete_query['metadata__filter1__in'] = spectral_line_ids
        additional_columns.add(MetadataColumn('Spectral Line', 'filter1'))

    if features:
        complete_query['tags__name__in'] = features
        additional_columns.add(TagColumn('Features'))

    if instrument and instrument != 'all':
        complete_query['instrument__name__iexact'] = instrument

    data_cubes = DataCube.objects.all()

    only_fields = ['oid', 'filename', 'instrument__name', 'metadata__date_beg', 'size', 'previews',
                   'spectral_line_data', *additional_columns.get_all_only_specs()]

    data_cubes = data_cubes.filter(freeform_query_q).filter(
        **complete_query).select_related('metadata', 'instrument', 'previews', 'spectral_line_data').only(
        *only_fields).distinct()

    results = [_create_search_result_from_metadata(request, cube, additional_columns) for cube in data_cubes]

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
