from django import forms


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
