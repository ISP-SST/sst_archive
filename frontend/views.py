import os

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from data_access.utils import schedule_archiving_of_files
from dataset.models import DataLocation
from tags.models import DataLocationTag
from .complex_filters import get_complex_filter
from .file_selection import toggle_selection_from_session, is_selected_in_session, load_selections
from .forms import SearchForm, get_initial_search_form, persist_search_form, RegistrationForm


def file_detail(request, filename):
    data_location = DataLocation.objects.select_related('animated_preview', 'thumbnail', 'metadata').get(
        file_name__iexact=filename)
    metadata = data_location.metadata

    metadata_fields = {field.verbose_name: field.value_from_object(metadata) for field in metadata._meta.get_fields()}

    # FIXME(daniel): We shouldn't need to pop these from the fields.
    metadata_fields.pop('fits header', None)
    metadata_fields.pop('ID', None)
    metadata_fields.pop('data location', None)
    metadata_fields.pop('Observation ID', None)

    context = {
        'data_location': data_location,
        'metadata': metadata,
        'metadata_dict': model_to_dict(metadata),
        'metadata_fields': metadata_fields,
    }

    return render(request, 'frontend/file_detail.html', context)


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


def _create_search_result_from_metadata(request, data_location, metadata, additional_columns):
    if hasattr(metadata.data_location, 'thumbnail'):
        thumbnail = metadata.data_location.thumbnail.image_url if metadata.data_location.thumbnail else None
    else:
        thumbnail = None

    attributes = [('metadata__', data_location.metadata), ('tags__', data_location.tags), ('', data_location)]
    additional_values = []

    for prefix, target_obj in attributes:
        additional_fields = [field_spec.removeprefix(prefix) for field_spec in
                             additional_columns.get_field_specs()
                             if field_spec.startswith(prefix)]
        additional_values += [getattr(target_obj, field) for field in additional_fields if
                              hasattr(target_obj, field)]

    return SearchResult(metadata.oid, data_location.file_name, data_location.instrument.name, metadata.date_beg,
                        metadata.data_location.file_size, thumbnail, additional_values,
                        is_selected_in_session(request, data_location.file_name))


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

    wavemin = None
    if 'wavemin' in form.cleaned_data and form.cleaned_data['wavemin'] != '':
        wavemin = form.cleaned_data['wavemin']

    wavemax = None
    if 'wavemax' in form.cleaned_data and form.cleaned_data['wavemax'] != '':
        wavemax = form.cleaned_data['wavemax']

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

    if wavemin:
        complete_query['metadata__wavelnth__gte'] = wavemin
    if wavemax:
        complete_query['metadata__wavelnth__lte'] = wavemax

    if features:
        complete_query['tags__tag__category__name__iexact'] = 'Features'
        complete_query['tags__tag__name__in'] = features
        additional_columns.add('Features', 'feature_tags', None)

    if instrument and instrument != 'all':
        complete_query['instrument__name__iexact'] = instrument

    data_locations = DataLocation.objects.all()

    data_locations = data_locations.filter(freeform_query_q).filter(
        **complete_query).select_related('metadata', 'instrument', 'thumbnail').prefetch_related('tags').only(
        'metadata__oid', 'file_name',
        'instrument__name',
        'metadata__date_beg',
        'file_size', 'thumbnail',
        *additional_columns.get_only_specs())

    if features:
        # FIXME(daniel): This subquery does not leave us with one row per file. If a file has multiple tags we
        #                now also get multiple rows for that file, but the "feature_tags" property is also not
        #                correctly set to represent the correct names of each of the tags.
        tags = DataLocationTag.objects.filter(tag__category__name__iexact='Features',
                                              data_location=OuterRef('pk')).values('tag__name')
        data_locations = data_locations.annotate(feature_tags=Subquery(tags))

    results = [_create_search_result_from_metadata(request, data_location, data_location.metadata, additional_columns)
               for data_location in
               data_locations]

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


def toggle_file_selection(request, filename):
    return_url = request.META.get('HTTP_REFERER', '/')
    toggle_selection_from_session(request, filename)
    return redirect(return_url)


def download_selected_data(request):
    selection_list = load_selections(request)

    ROOT_DIR = '/Users/dani2978/local_science_data'
    files = []

    file_list = list(map(lambda selection: selection.filename, selection_list))

    file_info_query = DataLocation.objects.filter(file_name__in=file_list).values_list(
        'data_location__file_path', 'data_location__file_name', 'data_location__file_size').iterator()
    files += [os.path.relpath(os.path.join(file_info[0], file_info[1]), ROOT_DIR) for file_info in file_info_query]

    id = schedule_archiving_of_files(ROOT_DIR, files)
    return HttpResponse(str(id), status=200)


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'frontend/account_register.html', {'registration_form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        if not form.is_valid():
            return render(request, 'frontend/account_register.html', {'registration_form': form})

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        new_user = User.objects.create_user(email, email, password)
        new_user.save()

        login(request, new_user)
        return redirect('/')
