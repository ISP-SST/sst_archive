from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from data_access.models import is_user_in_swedish_citizens_group, get_user_swedish_citizen_validation_status, \
    ValidationResult


def account_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    validation_status = get_user_swedish_citizen_validation_status(request.user)

    if validation_status == None:
        swedish_citizen = 'No'
    elif validation_status == ValidationResult.APPROVED:
        swedish_citizen = 'Approved'
    elif validation_status == ValidationResult.REJECTED:
        swedish_citizen = 'Rejected'
    elif validation_status == ValidationResult.NOT_PROCESSED:
        swedish_citizen = 'Under Review'

    context = {
        'user': request.user,
        'swedish_citizen': swedish_citizen
    }

    return render(request, 'frontend/account_profile.html', context)
