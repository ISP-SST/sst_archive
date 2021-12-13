import datetime
import json

from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from frontend.utils import get_memory_cache
from observations.models import Tag, Instrument


def initial_start_date():
    # Start date defaults to beginning of 2000.
    return datetime.datetime(2000, month=1, day=1)


def initial_end_date():
    return datetime.datetime.now()


def _get_query_label():
    return '<p>Advanced query <a class="bi bi-question-circle" ' + \
           'data-bs-toggle="tooltip" data-bs-html="true" href="#" ' + \
           'title="Allows for arbitrary queries into observation metadata.</p>' \
           '<p>Example: ' + \
           '<code>cubes__metadata__xposure__lt=0.15</code></p>' \
           '<p>This is an advanced feature and will likely not be suitable for ' \
           'most users.</p>"></a> '


def get_spectral_line_choices():
    cache = get_memory_cache()
    SPECTRAL_LINES_CACHE_KEY = 'known_spectral_line_choices'

    choices = cache.get(SPECTRAL_LINES_CACHE_KEY)

    if not choices:
        # Repopulate cache.
        from metadata.models import Metadata
        choices = [('%s' % (metadata[0]), '%s Å (%s)' % (metadata[0], metadata[1])) for
                   metadata in Metadata.objects.order_by('filter1').values_list('filter1', 'waveband').distinct()]
        cache.set(SPECTRAL_LINES_CACHE_KEY, choices)

    return choices


def get_features_choices():
    cache = get_memory_cache()
    FEATURES_CACHE_KEY = 'known_features'

    choices = cache.get(FEATURES_CACHE_KEY)

    if not choices:
        # Repopulate cache.
        tags = Tag.objects.all()
        choices = [(tag.name, tag.name) for tag in tags]
        cache.set(FEATURES_CACHE_KEY, choices)

    return choices


def get_instruments_choices():
    cache = get_memory_cache()
    INSTRUMENTS_CACHE_KEY = 'known_instruments'

    choices = cache.get(INSTRUMENTS_CACHE_KEY)

    if not choices:
        # Repopulate cache.
        instruments = Instrument.objects.all()
        choices = [('all', 'All')] + [(instrument.name.lower(), instrument.name) for instrument in instruments]
        cache.set(INSTRUMENTS_CACHE_KEY, choices)

    return choices


class DropdownCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'frontend/widgets/dropdown_checkbox_select.html'

    def __init__(self, attrs=None):
        if attrs:
            self.full_field_name = attrs.get('full_field_name', None)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        return {
            **super().get_context(name, value, attrs),
            'full_field_name': self.full_field_name
        }


class SearchForm(forms.Form):
    start_date = forms.DateField(label='Start Date',
                                 initial=initial_start_date,
                                 widget=forms.DateInput(format='%Y-%m-%d',
                                                        attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Select a date',
                                                            'type': 'date'}))
    end_date = forms.DateField(label='End Date',
                               initial=datetime.date.today,
                               widget=forms.DateInput(format='%Y-%m-%d',
                                                      attrs={
                                                          'class': 'form-control',
                                                          'placeholder': 'Select a date',
                                                          'type': 'date'}))
    instrument = forms.ChoiceField(label='Instrument',
                                   required=False,
                                   choices=get_instruments_choices,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    spectral_lines = forms.MultipleChoiceField(label='Spectral Lines',
                                               choices=get_spectral_line_choices,
                                               required=False,
                                               widget=DropdownCheckboxSelectMultiple(
                                                   attrs={
                                                       'full_field_name': 'Spectral Lines'
                                                   }
                                               ))
    # Re-add this field when the tags feature is implemented and launched.
    """
    features = forms.MultipleChoiceField(label='Features', choices=get_features_choices,
                                         required=False,
                                         widget=DropdownCheckboxSelectMultiple(attrs={
                                             'full_field_name': 'Features'
                                         }))
    """
    polarimetry = forms.ChoiceField(label='Polarimetry',
                                    required=True,
                                    choices=(('any', 'Any'),
                                             ('polarimetric', 'Polarimetric'),
                                             ('nonpolarimetric', 'Non-Polarimetric')),
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    advanced_query = forms.CharField(label=mark_safe(_get_query_label()), required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


def get_initial_search_form(request):
    return json.loads(request.session['search_form']) if 'search_form' in request.session else {}


def persist_search_form(request, cleaned_form_data):
    request.session['search_form'] = json.dumps(cleaned_form_data, cls=DjangoJSONEncoder)


def inject_search_form(request):
    initial = get_initial_search_form(request)
    return {'search_form': SearchForm(initial=initial)}
