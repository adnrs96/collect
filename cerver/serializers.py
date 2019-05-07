from rest_framework import serializers
from cerver.models import Form, Question

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('name', 'description')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('qheadline', 'qdescription', 'question_type', 'form')
