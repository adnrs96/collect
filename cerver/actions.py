from typing import List
from cerver.models import Form, Question, FormResponse, Response, FormOperation
from cerver.operations.operate import OPERATIONS_REGISTER
from django.db.models import F
from django.db import transaction

def do_create_form(name: str, description: str) -> Form:
    form = Form(name=name, description=description)
    form.save()
    return form

def do_create_question(qheadline: str,
                       form: Form,
                       qdescription: str='',
                       question_type: int=Question.TEXT) -> Question:
    question = Question(qheadline=qheadline,
                        qdescription=qdescription,
                        question_type=question_type,
                        form=form)
    with transaction.atomic():
        question.save()
        form.total_questions = F('total_questions') + 1
        form.save()
    return question

def do_create_form_response(form: Form) -> FormResponse:
    form_response = FormResponse(form=form)
    form_response.save()
    return form_response

def bulk_create_responses(responses: List[Response]) -> None:
    Response.objects.bulk_create(responses)

def do_attach_ops_to_forms(form: Form, ops: List[int]) -> None:
    form_ops = []
    res = []
    for op in ops:
        form_ops.append(
            FormOperation(
                form=form,
                operation_register_id=op,
                phase_type=OPERATIONS_REGISTER[op].get('phase_type', FormOperation.POST_BUSINESS)
            )
        )

    FormOperation.objects.bulk_create(form_ops)
