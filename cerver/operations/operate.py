from cerver.operations import export_to_googlesheets
from cerver.models import Form, FormOperation, get_all_responses

OPERATIONS_REGISTER = {
    # This is very sensitive part of the operations pipeline and shouldn't be
    # fiddled with unless you know what you are doing. Remember Newton's third law!
    1: {
        "name": "Export to Google Sheets",
        "script": export_to_googlesheets,
    },
}

def handle_post_business_logic(form: Form) -> None:
    post_business_ops = list(form.operations.filter(phase_type=FormOperation.POST_BUSINESS))

    # Ideally here we would want some kinda priority resolver so that we can
    # figure a order to apply operations in.
    ordered_ops = post_business_ops

    responses = get_all_responses(form)

    for op in ordered_ops:
        handler = OPERATIONS_REGISTER[op.operation_register_id]['script']
        responses, ok = handler.apply_operation(form, responses)

        if ok == '':
            raise 'Error Occured while performing ' + OPERATIONS_REGISTER[op.operation_register_id]['name']
