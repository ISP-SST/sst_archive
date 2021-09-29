from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from frontend.forms import RegistrationForm


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'frontend/account_register.html', {'registration_form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        if not form.is_valid():
            return render(request, 'frontend/account_register.html', {'registration_form': form})

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        new_user = User.objects.create_user(email, email, password)
        new_user.save()

        login(request, new_user)
        return redirect('/')
