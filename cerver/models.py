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

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(FormResponse)
admin.site.register(Response)
