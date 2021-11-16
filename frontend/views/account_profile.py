from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from data_access.models import get_user_swedish_user_validation_status, ValidationResult


def account_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    validation_status = get_user_swedish_user_validation_status(request.user)

    if validation_status == None:
        swedish_user = 'No'
    elif validation_status == ValidationResult.APPROVED:
        swedish_user = 'Approved'
    elif validation_status == ValidationResult.REJECTED:
        swedish_user = 'Rejected'
    elif validation_status == ValidationResult.NOT_PROCESSED:
        swedish_user = 'Under Review'

    context = {
        'user': request.user,
        'swedish_user': swedish_user
    }

    return render(request, 'frontend/account_profile.html', context)
