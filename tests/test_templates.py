from flask_passwordless.templates import MessageTemplate
import os

config = {
    "TEMPLATES": {
        "TEMPLATE_PATH": os.path.join(os.getcwd(), 'tests'),
        "TEMPLATE_FILE": "test.html"
    }
}


def test_template():
    email_tmpl = MessageTemplate(config)
    right_answer = "The answer is: blah"
    tmpl_string = email_tmpl({"answer": "blah"})
    assert right_answer == tmpl_string
