from django import forms
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json


def initial_start_date():
    return datetime.date.today() - datetime.timedelta(weeks=52)


class SearchForm(forms.Form):
    start_date = forms.DateField(label='Start', initial=initial_start_date, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}))
    end_date = forms.DateField(label='End', initial=datetime.date.today, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}))
    dataset = forms.ChoiceField(label='Datasets', choices=(('all', 'All'), ('chromis', 'CHROMIS'), ('crisp', 'CRISP')), widget=forms.Select(attrs={'class':'form-select'}))
    query = forms.CharField(label='Query', initial='', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


def get_initial_search_form(request):
    return json.loads(request.session['search_form']) if 'search_form' in request.session else {}


def persist_search_form(request, cleaned_form_data):
    request.session['search_form'] = json.dumps(cleaned_form_data, cls=DjangoJSONEncoder)


def inject_search_form(request):
    initial = get_initial_search_form(request)
    return {'search_form': SearchForm(initial=initial)}
