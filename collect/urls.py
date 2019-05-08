"""collect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cerver.views.forms import (
    handle_response_backend,
    handle_form_creation,
    handle_form_add_question,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('collect/forms', handle_form_creation),
    path('collect/forms/<int:form_id>/add_question', handle_form_add_question),
    path('collect/forms/<int:form_id>/response', handle_response_backend),
]
