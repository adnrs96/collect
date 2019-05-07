from rest_framework import serializers
from cerver.models import Form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('name', 'description')
