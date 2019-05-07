from typing import List
from cerver.models import Form, Question, FormResponse, Response
from django.db.models import F

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
    question.save()
    form.update(total_questions=F('total_questions') + 1)
    return question

def do_create_form_response(form: Form) -> FormResponse:
    form_response = FormResponse(form=form)
    form_response.save()
    return form_response

def bulk_create_responses(responses: List[Response]) -> None:
    Response.objects.bulk_create(responses)
