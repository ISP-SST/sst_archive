import datetime
import json

from django import forms
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


def initial_start_date():
    # Start date defaults to three years back.
    today = datetime.date.today()
    return today.replace(year=today.year - 3)


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
    dataset = forms.ChoiceField(label='Instrument',
                                choices=(('all', 'All'), ('chromis', 'CHROMIS'), ('crisp', 'CRISP')),
                                widget=forms.Select(attrs={'class': 'form-select'}))
    wavemin = forms.FloatField(label='Min Wavelength', widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               required=False)
    wavemax = forms.FloatField(label='Max Wavelength', widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               required=False)
    polarimetry = forms.ChoiceField(label='Polarimetry',
                                     choices=(('any', 'Any'),
                                              ('polarimetric', 'Polarimetric'),
                                              ('nonpolarimetric', 'Non-Polarimetric')),
                                     widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    query = forms.CharField(label='Query', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


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
    request.session['search_form'] = json.dumps(cleaned_form_data, cls=DjangoJSONEncoder)


def inject_search_form(request):
    initial = get_initial_search_form(request)
    return {'search_form': SearchForm(initial=initial)}
