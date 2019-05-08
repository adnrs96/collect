from django.http import HttpRequest, HttpResponse, JsonResponse
from cerver.operations.operate import handle_post_business_logic
from cerver.models import get_form_by_id
import json

def handle_post_busines_backend(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res

    form = get_form_by_id(form_id)
    if form is None:
        res = JsonResponse({'msg': 'Form not found.'})
        res.status_code = 404
        return res

    # In future we could potentially make use of POST data for figuring if we
    # wanna exclude/include some ops apart from what's in the FormOperation

    handle_post_business_logic(form)

    res = JsonResponse({'msg': 'Success'})
    res.status_code = 200
    return res
