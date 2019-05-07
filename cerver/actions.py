from cerver.models import Form, Question

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
    return question
