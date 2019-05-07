from django.db import models
from django.contrib import admin

# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

admin.site.register(Form)
