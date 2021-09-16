import json


_SELECTION_KEY = 'metadata_selection'


def new_selection(filename):
    return {"filename": filename}


def load_selections(request):
    try:
        selection = request.session[_SELECTION_KEY]
    except KeyError:
        selection = "[]"
    selection_array = json.loads(selection)
    return selection_array


def _persist_selections(request, selections):
    request.session[_SELECTION_KEY] = json.dumps(selections)


def is_selected_in_session(request, filename):
    selections = load_selections(request)
    return new_selection(filename) in selections


def add_selection_to_session(request, filename):
    selections = load_selections(request)

    changed_selection = new_selection(filename)

    if changed_selection not in selections:
        selections.append(changed_selection)

    _persist_selections(request, selections)


def remove_selection_from_session(request, filename):
    selections = load_selections(request)

    changed_selection = new_selection(filename)

    if changed_selection in selections:
        selections.remove(changed_selection)

    _persist_selections(request, selections)


def toggle_selection_from_session(request, filename):
    selections = load_selections(request)

    changed_selection = new_selection(filename)
    is_now_on = False

    if changed_selection in selections:
        selections.remove(changed_selection)
    else:
        selections.append(changed_selection)
        is_now_on = True

    _persist_selections(request, selections)

    return is_now_on


def inject_selection_list(request):
    selection_list = load_selections(request)

    return {"selection_list": selection_list}
