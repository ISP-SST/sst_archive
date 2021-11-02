import datetime
import json

from django import forms
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from frontend.utils import get_memory_cache
from observations.models import Tag, Instrument


def initial_start_date():
    # Start date defaults to three years back.
    today = datetime.datetime.now(tz=datetime.timezone.utc)
    return today.replace(year=today.year - 3)


def initial_end_date():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def _get_query_label():
    return 'Query <a class="bi bi-question-circle" ' + \
           'data-bs-toggle="tooltip" data-bs-html="true" href="#" ' + \
           'title="Allows for arbitrary queries into observation metadata: ' + \
           '<code>metadata__xposure__lt=0.15</code>"></a> '


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


class SelectWidgetWithTooltip(forms.Select):
    option_template_name = 'frontend/widgets/select_option_with_tooltip.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context


def create_download_form(download_choices):
    class DownloadCubesForm(forms.Form):
        files = forms.MultipleChoiceField(label='', choices=download_choices,
                                          widget=SelectWidgetWithTooltip(attrs={
                                              'class': 'form-select',
                                              'size': 5
                                          }))
    return DownloadCubesForm()


class SearchForm(forms.Form):
    start_date = forms.DateField(label='Start Date',
                                 initial=initial_start_date,
                                 widget=forms.DateInput(format=('%Y-%m-%d'),
                                                        attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Select a date',
                                                            'type': 'date'}))
    end_date = forms.DateField(label='End Date',
                               initial=datetime.date.today,
                               widget=forms.DateInput(format=('%Y-%m-%d'),
                                                      attrs={
                                                          'class': 'form-control',
                                                          'placeholder': 'Select a date',
                                                          'type': 'date'}))
    instrument = forms.ChoiceField(label='Instrument',
                                   choices=get_instruments_choices,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    spectral_lines = forms.MultipleChoiceField(label='Spectral Lines',
                                               choices=get_spectral_line_choices,
                                               widget=DropdownCheckboxSelectMultiple(
                                                   attrs={
                                                       'full_field_name': 'Spectral Lines'
                                                   }
                                               ))
    features = forms.MultipleChoiceField(label='Features', choices=get_features_choices,
                                         widget=DropdownCheckboxSelectMultiple(attrs={
                                             'full_field_name': 'Features'
                                         }))
    polarimetry = forms.ChoiceField(label='Polarimetry',
                                    choices=(('any', 'Any'),
                                             ('polarimetric', 'Polarimetric'),
                                             ('nonpolarimetric', 'Non-Polarimetric')),
                                    widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    query = forms.CharField(label=mark_safe(_get_query_label()), required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_css_class = "alert alert-danger"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match'
            )

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail %s is already registered' % email)


def get_initial_search_form(request):
    return json.loads(request.session['search_form']) if 'search_form' in request.session else {}


def persist_search_form(request, cleaned_form_data):
    # request.session['search_form'] = serializers.serialize("json", cleaned_form_data)
    request.session['search_form'] = json.dumps(cleaned_form_data, cls=DjangoJSONEncoder)


def inject_search_form(request):
    initial = get_initial_search_form(request)
    return {'search_form': SearchForm(initial=initial)}
