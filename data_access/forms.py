from django import forms


class TokenForm(forms.Form):
    token = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'font-family: monospace'}))
