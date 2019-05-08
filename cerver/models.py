from typing import List
from django.db import models
from django.contrib import admin

# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    total_questions = models.PositiveSmallIntegerField(default=0)

class FormResponse(models.Model):
    form = models.ForeignKey(
        Form,
        related_name='responses',
        on_delete=models.CASCADE
    )
    is_response_stored = models.BooleanField(default=False)

class Question(models.Model):
    qheadline = models.CharField(max_length=150)
    qdescription = models.CharField(max_length=500, blank=True)

    TEXT = 1
    INT = 2
    BOOL = 3

    QUESTION_TYPES = (
        (TEXT, 'Input text to answer'),
        (INT, 'Input an Integer to answer'),
        (BOOL, 'Select from True/False'),
    )

    question_type = models.PositiveSmallIntegerField(
        choices=QUESTION_TYPES,
        default=TEXT
    )

    form = models.ForeignKey(
        Form,
        related_name='form_questions',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (self.qheadline + '\n' + self.qdescription).strip()

class Response(models.Model):
    form_response = models.ForeignKey(
        FormResponse,
        related_name='answers',
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        related_name='responses',
        on_delete=models.CASCADE
    )

    value = models.CharField(max_length=1000, blank=True)

    class Meta:
        unique_together = (('form_response', 'question'),)

class FormOperation(models.Model):
    form = models.ForeignKey(
        Form,
        related_name='operations',
        on_delete=models.CASCADE
    )
    operation_register_id = models.PositiveSmallIntegerField(default=0)

    VALIDATION = 1
    POST_VALIDATION = 2
    POST_BUSINESS = 3

    PHASE_TYPES = (
        (VALIDATION, 'Operation(s) executes on validation stage before any response is stored.'),
        (POST_VALIDATION, 'Operation(s) executes immediately after storage is successful.'),
        (POST_BUSINESS, 'Operation(s) Triggered by specific command and executes on Response Collective'),
    )

    phase_type = models.PositiveSmallIntegerField(
        choices=PHASE_TYPES,
        default=POST_BUSINESS
    )

def get_form_by_id(id: int) -> Form:
    return Form.objects.filter(id=id).first()

def get_all_responses(form: Form) -> List[List[Response]]:
    form_responses = list(form.responses.all())

    responses = []

    for form_response in form_responses:
        responses.append(list(form_response.answers.all()))

    return responses

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(FormResponse)
admin.site.register(Response)
