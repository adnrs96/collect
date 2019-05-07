from django.db import models
from django.contrib import admin

# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

class Question(models.Model):
    qheadline = models.CharField(max_length=150)
    qdescription = models.CharField(max_length=500)

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

admin.site.register(Form)
admin.site.register(Question)
