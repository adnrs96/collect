from cerver.models import Form

def do_create_form(name: str, description: str) -> Form:
    form = Form(name=name, description=description)
    form.save()
    return form
