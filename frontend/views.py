from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from dataset.models import Dataset, DataLocation
from data_access.utils import DataSelectionZipIterator, schedule_archiving_of_files
# from .complex_filters import get_complex_filter, InvalidFilterError
from .file_selection import toggle_selection_from_session, is_selected_in_session, load_selections
from .forms import SearchForm, get_initial_search_form, persist_search_form, RegistrationForm


class DatasetListView(ListView):
    model = Dataset
    paginate_by = 50
    template_name = 'frontend/dataset_list.html'
    context_object_name = 'dataset_list'


def dataset_detail(request, dataset):
    dataset = Dataset.objects.get(name__iexact=dataset)
    metadata_list =  dataset.metadata_model.objects.all()

    paginator = Paginator(metadata_list, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'dataset': dataset,
        'metadata': metadata_list,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'frontend/dataset_detail.html', context)


def metadata_detail(request, dataset, oid):
    dataset = Dataset.objects.get(name__iexact=dataset)
    metadata = dataset.metadata_model.objects.get(oid=oid)

    metadata_fields = {field.verbose_name: field.value_from_object(metadata) for field in metadata._meta.get_fields()}

    metadata_fields.pop('fits header', None)
    metadata_fields.pop('ID', None)
    metadata_fields.pop('data location', None)
    metadata_fields.pop('Observation ID', None)

    context = {
        'dataset': dataset,
        'metadata': metadata,
        'metadata_dict': model_to_dict(metadata),
        'metadata_fields': metadata_fields,
    }

    return render(request, 'frontend/metadata_detail.html', context)


class SearchResult:
    def __init__(self, oid, dataset, date, file_size, thumbnail, selected=False):
        self.oid = oid
        self.dataset = dataset
        self.date = date
        self.file_size = file_size
        self.thumbnail = thumbnail
        self.selected = selected


def _create_search_result_from_metadata(request, dataset, metadata):
    if hasattr(metadata.data_location, 'thumbnail'):
        thumbnail = metadata.data_location.thumbnail.image_url if metadata.data_location.thumbnail else None
    else:
        thumbnail = None

    return SearchResult(metadata.oid, dataset.name, metadata.date_beg,
                        metadata.data_location.file_size, thumbnail,
                        is_selected_in_session(request, dataset.name, metadata.oid))


def search_view(request):
    form = SearchForm(request.GET)

    if not form.is_valid():
        # TODO(daniel): Handle this error case.
        pass

    if not hasattr(form, 'cleaned_data') or  'start_date' not in form.cleaned_data:
        form = SearchForm(data=get_initial_search_form(request))
        form.full_clean()

    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    dataset = form.cleaned_data['dataset']

    query = form.cleaned_data['query']
    extra_query_args = {}
    """
    try:
        other_parsed_query = get_complex_filter(query)
        extra_query_args = other_parsed_query.children
    except InvalidFilterError:
        pass
    """

    if len(query) > 0:
        query_parts = query.split(',')
        extra_query_args = {part.split('=')[0]: part.split('=')[1] for part in query_parts}

    results = []

    persist_search_form(request, form.cleaned_data)

    dataset_query = Dataset.objects.all() if dataset == 'all' else Dataset.objects.filter(name__iexact=dataset)

    date_query = {'date_beg__gte': start_date, 'date_end__lte': end_date}
    complete_query = { **extra_query_args, **date_query }

    for dataset_obj in dataset_query:
        metadata_list = dataset_obj.metadata_model.objects.filter(**complete_query).prefetch_related('data_location').prefetch_related('data_location__thumbnail')
        results += [_create_search_result_from_metadata(request, dataset_obj, metadata) for metadata in metadata_list]

    paginator = Paginator(results, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'search_results': results,
        'paginator': paginator,
        'page_obj': page_obj,
    }

    return render(request, 'frontend/search_results.html', context)


def toggle_metadata_selection(request, dataset, oid):
    return_url = request.META.get('HTTP_REFERER', '/')
    toggle_selection_from_session(request, dataset, oid)
    return redirect(return_url)


def download_selected_data(request):
    selection_list = load_selections(request)

    selection_map = {}
    for selection in selection_list:
        dataset = selection['dataset']
        oid = selection['oid']

        if dataset not in selection_map:
            selection_map[dataset] = []

        selection_map[dataset].append(oid)

    ROOT_DIR = '/Users/dani2978/local_science_data'
    files = []

    import os
    for dataset, oids in selection_map.items():
        file_info_query = Dataset.objects.get(name__iexact=dataset).metadata_model.objects.filter(
            oid__in=oids).values_list('data_location__file_path', 'data_location__file_name',
                                      'data_location__file_size').iterator()
        files += [os.path.relpath(os.path.join(file_info[0], file_info[1]), ROOT_DIR) for file_info in file_info_query]

    id = schedule_archiving_of_files(ROOT_DIR, files)
    return HttpResponse(str(id), status=200)


def access_denied(request):
    return render(request, 'frontend/access_denied.html', {})


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

