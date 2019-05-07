from django.http import HttpRequest, HttpResponse, JsonResponse
from cerver.serializers import FormSerializer
from cerver.actions import do_create_form
import json

def handle_response_backend(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res
    print(json.loads(request.body))
    res = JsonResponse({'msg': 'Reached code to execute save'})
    res.status_code = 200
    return res

def handle_form_creation(request: HttpRequest):
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res

    new_formdata = FormSerializer(data=json.loads(request.body))
    if not new_formdata.is_valid():
        error_msg = {'msg': 'error'}
        error_msg.update(new_formdata.errors)
        res = JsonResponse(error_msg)
        res.status_code = 400
        return res

    data = new_formdata.validated_data
    new_form = do_create_form(data['name'], data['description'])

    res = JsonResponse({'msg': 'Form created.', 'form_id': new_form.id})
    res.status_code = 200
    return res
