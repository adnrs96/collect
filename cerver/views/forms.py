from django.http import HttpRequest, HttpResponse, JsonResponse
from cerver.serializers import FormSerializer, QuestionSerializer
from cerver.actions import (
    do_create_form, do_create_question, do_create_form_response,
    bulk_create_responses, do_attach_ops_to_forms
)
from django.db import transaction
from cerver.models import Question, get_form_by_id, Response
from cerver.operations.operate import OPERATIONS_REGISTER
import json

def handle_form_op(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res
    form = get_form_by_id(form_id)
    if form is None:
        res = JsonResponse({'msg': 'Form not found.'})
        res.status_code = 404
        return res

    data = json.loads(request.body)
    if data['form_id'] != str(form_id):
        res = JsonResponse({'msg': 'Form Mismatch.'})
        res.status_code = 400
        return res

    ops = list(map(int, data["ops"]))
    all_form_ops = list(map(lambda x: x.operation_register_id, list(form.operations.all())))
    for op in ops:
        if op not in OPERATIONS_REGISTER or op in all_form_ops:
            res = JsonResponse({'msg': 'Invalid or duplicate op.'})
            res.status_code = 400
            return res


    do_attach_ops_to_forms(form, ops)
    data = {
        'msg': 'success',
    }
    res = JsonResponse(data)
    res.status_code = 200
    return res

def handle_form_display(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'GET':
        res = JsonResponse({'msg': 'Only GET requests accepted.'})
        res.status_code = 403
        return res

    form = get_form_by_id(form_id)
    if form is None:
        res = JsonResponse({'msg': 'Form not found.'})
        res.status_code = 404
        return res

    form_questions = list(form.form_questions.all())
    questions = []
    for form_question in form_questions:
        questions.append(
            {
                'qid': form_question.id,
                'qhead': form_question.qheadline,
                'qdesc': form_question.qdescription,
                'qtype': form_question.question_type,
            }
        )

    data = {
        'msg': 'success',
        'id': form.id,
        'name': form.name,
        'description': form.description,
        'questions': questions,
    }

    res = JsonResponse(data)
    res.status_code = 200
    return res

def handle_response_backend(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res
    form = get_form_by_id(form_id)
    if form is None:
        res = JsonResponse({'msg': 'Form not found.'})
        res.status_code = 404
        return res

    form_response = do_create_form_response(form)

    data = json.loads(request.body)
    response_dict = data[str(form_id)]
    form_questions = list(form.form_questions.all())
    responses = []

    if len(form_questions) != len(response_dict):
        res = JsonResponse({'msg': 'Invalid Form submission'})
        res.status_code = 400
        return res

    for q_id, value in response_dict.items():
        # Since number of questions in a form in real world are going to be
        # pretty much in the range of 100 at most we will just use a linear
        # search without adding too much CPU time.
        status = 1
        for question in form_questions:
            if question.id == int(q_id):
                try:
                    response = Response(form_response=form_response,
                                        question=question,
                                        value=value)
                except:
                    res = JsonResponse({'msg': 'Invalid Form submission'})
                    res.status_code = 400
                    return res

                responses.append(response)
                status = 0
                break
        if status:
            res = JsonResponse({'msg': 'Invalid Form submission'})
            res.status_code = 400
            return res

    with transaction.atomic():
        bulk_create_responses(responses)
        form_response.update(is_response_stored=True)
    res = JsonResponse({'msg': 'Response stored.', 'form_response_id': form_response.id})
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

def handle_form_add_question(request: HttpRequest, form_id: int) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 403
        return res

    new_questiondata = QuestionSerializer(data=json.loads(request.body))
    if not new_questiondata.is_valid():
        error_msg = {'msg': 'error'}
        error_msg.update(new_questiondata.errors)
        res = JsonResponse(error_msg)
        res.status_code = 400
        return res

    data = new_questiondata.validated_data
    if data['form'].id != form_id:
        res = JsonResponse({'msg': 'Form Mismatch.'})
        res.status_code = 400
        return res

    qheadline = data['qheadline']
    qdescription = data.get('qdescription', '')
    question_type = data.get('question_type', Question.TEXT)
    form = data['form']
    new_question = do_create_question(qheadline, form, qdescription, question_type)

    res = JsonResponse({'msg': 'Question created.', 'question_id': new_question.id})
    res.status_code = 200
    return res
