from allauth.account.forms import ResetPasswordForm, ChangePasswordForm, ResetPasswordKeyForm
from captcha.fields import ReCaptchaField
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from core.account import EmailVerificationEnforcingLoginForm, ExtendedSignupForm
from data_access.models import enqueue_swedish_user_registration_request
from frontend.utils import add_bootstrap_form_classes_to_fields

SWEDISH_USER_HELP_TEXT = '<strong>IMPORTANT:</strong> By specifying that you are a Swedish user your acount will ' \
                         'be put through a manual verification process before you will be able to access data ' \
                         'generated by Swedish Universities. If you are not a Swedish citizen or affiliated ' \
                         'with a Swedish university, do not check this box.'

PURPOSE_HELP_TEXT = 'Please provide a brief description of the purpose for the account, e.g. what type of data you ' \
                    'are interested in.'

REQUIRED_SUFFIX = mark_safe(' <span class="text-primary">*</span>')


class CustomErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        else:
            return '<div class="alert alert-warning">%s</div>' % ''.join(
                ['<div class="error"><i class="bi bi-exclamation-circle-fill"></i> %s</div>' % e for e in self])


class CustomLoginForm(EmailVerificationEnforcingLoginForm):
    error_css_class = 'alert alert-warning'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
        add_bootstrap_form_classes_to_fields(self.fields)


class CustomResetPasswordForm(ResetPasswordForm):
    field_order = ['email', 'password1', 'password2', 'swedish_user', 'captcha']

    error_css_class = 'alert alert-warning'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
        add_bootstrap_form_classes_to_fields(self.fields)


class CustomSignupForm(ExtendedSignupForm):
    field_order = ['email', 'password1', 'password2', 'first_name', 'last_name', 'affiliation', 'purpose',
                   'swedish_user', 'captcha']

    error_css_class = 'alert alert-warning'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
        add_bootstrap_form_classes_to_fields(self.fields)

        for field_name in self.fields:
            field = self.fields[field_name]
            if field.required:
                field.label_suffix = field.label_suffix + REQUIRED_SUFFIX if field.label_suffix is not None \
                    else REQUIRED_SUFFIX

    def save(self, request):
        user = super().save(request)

        swedish_user = self.cleaned_data.get('swedish_user')

        # Enqueue the user for manual validation of Swedish credentials.
        if swedish_user:
            enqueue_swedish_user_registration_request(user)

        return user

    captcha = ReCaptchaField(label=False)


class CustomChangePasswordForm(ChangePasswordForm):
    error_css_class = 'alert alert-warning'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
        add_bootstrap_form_classes_to_fields(self.fields)


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    error_css_class = 'alert alert-warning'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
        add_bootstrap_form_classes_to_fields(self.fields)
