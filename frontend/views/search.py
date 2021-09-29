from django.core.paginator import Paginator
from django.shortcuts import render

from observations.models import DataCube
from frontend.complex_filters import get_complex_filter
from frontend.file_selection import is_selected_in_session
from frontend.forms import SearchForm, get_initial_search_form, persist_search_form


# Compatibility function. Was introduced in Python 3.9, but we're currently only on 3.7.
def removeprefix(self, prefix):
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


class SearchResult:
    def __init__(self, oid, filename, instrument, date, file_size, thumbnail, additional_values, selected=False):
        self.oid = oid
        self.filename = filename
        self.instrument = instrument
        self.date = date
        self.file_size = file_size
        self.thumbnail = thumbnail
        self.selected = selected
        self.additional_values = additional_values


def _create_search_result_from_metadata(request, cube, additional_columns):
    if not hasattr(cube, 'metadata') or not cube.metadata:
        return None

    if hasattr(cube, 'thumbnail'):
        thumbnail = cube.thumbnail.image_url if cube.thumbnail else None
    else:
        thumbnail = None

    attributes = [('metadata__', cube.metadata), ('', cube)]
    additional_values = []

    for prefix, target_obj in attributes:
        additional_fields = [removeprefix(field_spec, prefix) for field_spec in
                             additional_columns.get_field_specs()
                             if field_spec.startswith(prefix)]
        additional_values += [getattr(target_obj, field) for field in additional_fields if
                              hasattr(target_obj, field)]

    return SearchResult(cube.oid, cube.filename, cube.instrument.name,
                        cube.metadata.date_beg, cube.size, thumbnail, additional_values,
                        is_selected_in_session(request, cube.filename))


class AdditionalColumns:
    class Column():
        def __init__(self, column_name, column_field_spec, column_only_spec=''):
            self.column_name = column_name
            self.column_field_spec = column_field_spec
            if column_only_spec == '':
                self.column_only_spec = column_field_spec
            else:
                self.column_only_spec = column_only_spec

    def __init__(self):
        self.additional_columns = []

    def add(self, column_name, column_field_spec, column_only_spec):
        self.additional_columns.append(self.Column(column_name, column_field_spec, column_only_spec))

    def get_names(self):
        return [col.column_name for col in self.additional_columns if col.column_name != None]

    def get_field_specs(self):
        return [col.column_field_spec for col in self.additional_columns if col.column_field_spec != None]

    def get_only_specs(self):
        return [col.column_only_spec for col in self.additional_columns if col.column_only_spec != None]


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
        complete_query['metadata__date_beg__gte'] = start_date
    if end_date:
        complete_query['metadata__date_end__lte'] = end_date

    if spectral_line_ids:
        complete_query['metadata__filter1__in'] = spectral_line_ids
        additional_columns.add('Spectral Line', 'metadata__filter1', 'metadata__filter1')

    if features:
        complete_query['tags__tag__category__name__iexact'] = 'Features'
        complete_query['tags__tag__name__in'] = features
        additional_columns.add('Features', 'feature_tags', None)

    if instrument and instrument != 'all':
        complete_query['instrument__name__iexact'] = instrument

    data_cubes = DataCube.objects.all()

    data_cubes = data_cubes.filter(freeform_query_q).filter(
        **complete_query).select_related('metadata', 'instrument', 'thumbnail') .only(
        'oid', 'filename',
        'instrument__name',
        'metadata__date_beg',
        'size', 'thumbnail',
        *additional_columns.get_only_specs())

    """
    if features:
        # FIXME(daniel): This subquery does not leave us with one row per file. If a file has multiple tags we
        #                now also get multiple rows for that file, but the "feature_tags" property is also not
        #                correctly set to represent the correct names of each of the tags.
        tags = DataLocationTag.objects.filter(tag__category__name__iexact='Features',
                                              data_location=OuterRef('pk')).values('tag__name')
        data_locations = data_cubes.annotate(feature_tags=Subquery(tags))
    """

    results = [_create_search_result_from_metadata(request, cube, additional_columns) for cube in data_cubes]

    results = list(filter(None, results))

    paginator = Paginator(results, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'search_results': results,
        'paginator': paginator,
        'page_obj': page_obj,
        'additional_column_names': additional_columns.get_names(),
    }

    return render(request, 'frontend/search_results.html', context)
