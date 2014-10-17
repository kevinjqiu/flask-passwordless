import mandrill
from flask import url_for


class DeliveryMethod(object):
    def __call__(self, token, userid, **kwargs):
        pass


class DeliverByMandrill(DeliveryMethod):
    def __init__(self, config):
        api_key = config.get('MANDRILL_API_KEY')
        self.mandrill = mandrill.Mandrill(api_key)

    def __call__(self, token, userid, email):
        url = "".join([
            'http://localhost:5000',
            url_for('authenticate'),
            "?token={}&uid={}".format(token, userid)
        ])
        message = dict(
            text=url,
            from_email='flask-passwordless@example.com',
            to=[{
                'email': email,
                'type': 'to',
            }],
            subject='Your login info',
        )
        self.mandrill.messages.send(message=message)
