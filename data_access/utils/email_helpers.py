from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

EMAIL_SUBJECT = 'Swedish user registration update'


def send_swedish_user_registration_admin_notice(request):
    template = get_template('data_access/email/swedish_user_registration_notice.txt')
    email_body = template.render({
        'request': request,
        'hostname': settings.HOSTNAME,
    })
    send_mail(EMAIL_SUBJECT, email_body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_SYSTEM_NOTIFICATION_EMAIL],
              fail_silently=True)
