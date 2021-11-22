from django.conf import settings


def contact_information(request):
    return {'contact_email': settings.DEFAULT_CONTACT_EMAIL}
