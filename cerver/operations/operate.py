from cerver.operations import export_to_googlesheets

OPERATIONS_REGISTER = {
    # This is very sensitive part of the operations pipeline and shouldn't be
    # fiddled with unless you know what you are doing. Remember Newton's third law!
    1: {
        "name": "Export to Google Sheets",
        "script": export_to_googlesheets,
    },
}
