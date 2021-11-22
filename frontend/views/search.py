from django.shortcuts import render

from frontend.utils import get_complex_filter
from frontend.forms import SearchForm, get_initial_search_form, persist_search_form
from search.search import SearchCriteria, search_observations


# Compatibility function. Was introduced in Python 3.9, but we're currently only on 3.7.
def removeprefix(self, prefix):
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


def search_view(request):
    form = SearchForm(request.GET)

    if not form.is_valid():
        # Just ignore this error. This should never happen in practice, but a call to is_valid() is required in order
        # to get the cleaned_data from the form.
        pass

    if not hasattr(form, 'cleaned_data') or 'start_date' not in form.cleaned_data:
        form = SearchForm(data=get_initial_search_form(request))
        form.full_clean()

    search_criteria = SearchCriteria()

    instrument = form.cleaned_data['instrument'] if 'instrument' in form.cleaned_data else 'all'
    if instrument and instrument != 'all':
        search_criteria.instrument = instrument

    if 'spectral_lines' in form.cleaned_data and form.cleaned_data['spectral_lines'] != '':
        spectral_lines = form.cleaned_data['spectral_lines']
        spectral_line_ids = [int(sl) for sl in spectral_lines]
        if spectral_line_ids:
            search_criteria.spectral_line_ids = spectral_line_ids

    if 'features' in form.cleaned_data and form.cleaned_data['features']:
        search_criteria.features = form.cleaned_data['features']

    query = form.cleaned_data['query']
    freeform_query_q = get_complex_filter(query)

    if 'polarimetry' in form.cleaned_data:
        search_criteria.polarimetry = form.cleaned_data['polarimetry']

    search_criteria.start_date = form.cleaned_data['start_date'] if 'start_date' in form.cleaned_data else None
    search_criteria.end_date = form.cleaned_data['end_date'] if 'end_date' in form.cleaned_data else None

    persist_search_form(request, form.cleaned_data)

    page_number = request.GET.get('page', 1)
    results = search_observations(search_criteria, page_number=page_number, complex_query=freeform_query_q)

    context = {
        'page_search_results': results.page,
        'paginator': results.page.paginator,
        'page_obj': results.page,
        'additional_column_names': results.additional_columns.get_all_names(),
    }

    return render(request, 'frontend/search_results.html', context)
