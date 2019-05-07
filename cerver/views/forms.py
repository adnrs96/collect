from django.http import HttpRequest, HttpResponse, JsonResponse

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
