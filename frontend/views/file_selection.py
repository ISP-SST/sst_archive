from django.shortcuts import redirect

from frontend.file_selection import toggle_selection_from_session


def toggle_file_selection(request, filename):
    return_url = request.META.get('HTTP_REFERER', '/')
    toggle_selection_from_session(request, filename)
    return redirect(return_url)
