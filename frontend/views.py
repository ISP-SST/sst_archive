import os

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from data_access.utils import schedule_archiving_of_files
from dataset.models import DataLocation, Instrument
from .complex_filters import get_complex_filter
from .file_selection import toggle_selection_from_session, is_selected_in_session, load_selections
from .forms import SearchForm, get_initial_search_form, persist_search_form, RegistrationForm


def file_detail(request, filename):
    data_location = DataLocation.objects.select_related('animated_preview', 'thumbnail').get(file_name__iexact=filename)
    metadata = data_location.instrument.metadata_model.objects.get(data_location=data_location)

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
    def __init__(self, oid, filename, instrument, date, file_size, thumbnail, selected=False):
        self.oid = oid
        self.filename = filename
        self.instrument = instrument
        self.date = date
        self.file_size = file_size
        self.thumbnail = thumbnail
        self.selected = selected


def _create_search_result_from_metadata(request, data_location, metadata):
    if hasattr(metadata.data_location, 'thumbnail'):
        thumbnail = metadata.data_location.thumbnail.image_url if metadata.data_location.thumbnail else None
    else:
        thumbnail = None

    return SearchResult(metadata.oid, data_location.file_name, data_location.instrument.name, metadata.date_beg,
                        metadata.data_location.file_size, thumbnail,
                        is_selected_in_session(request, data_location.file_name))


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

    wavemin = None
    if 'wavemin' in form.cleaned_data and form.cleaned_data['wavemin'] != '':
        wavemin = form.cleaned_data['wavemin']

    wavemax = None
    if 'wavemax' in form.cleaned_data and form.cleaned_data['wavemax'] != '':
        wavemax = form.cleaned_data['wavemax']

    polarimetry_query = {}
    if 'polarimetry' in form.cleaned_data:
        pol = form.cleaned_data['polarimetry']
        if pol == 'polarimetric':
            polarimetry_query['naxis4__exact'] = 4
        elif pol == 'nonpolarimetric':
            polarimetry_query['naxis4__exact'] = 1

    query = form.cleaned_data['query']
    freeform_query_q = get_complex_filter(query)

    results = []

    persist_search_form(request, form.cleaned_data)

    date_query = {}
    if start_date:
        date_query['date_beg__gte'] = start_date
    if end_date:
        date_query['date_end__lte'] = end_date

    complete_query = {**date_query, **polarimetry_query}

    # TODO(daniel): wavemin + wavemax query is incorrect.
    if wavemin:
        complete_query['wavelnth__gte'] = wavemin
    if wavemax:
        complete_query['wavelnth__lte'] = wavemax

    instruments_queryset = Instrument.objects.all()
    if instrument != 'all':
        instruments_queryset = instruments_queryset.filter(name__iexact=instrument)

    for instrument in instruments_queryset:
        metadata_list = instrument.metadata_model.objects.filter(freeform_query_q).filter(
            **complete_query).select_related(
            'data_location', 'data_location__instrument', 'data_location__thumbnail')
        results += [_create_search_result_from_metadata(request, metadata.data_location, metadata) for metadata in
                    metadata_list]

    paginator = Paginator(results, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'search_results': results,
        'paginator': paginator,
        'page_obj': page_obj,
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
