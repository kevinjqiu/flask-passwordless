import abc
from templates import MessageTemplate

class DeliveryMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, login_url, **kwargs):
        return


class DeliveryError(StandardError):
    pass


class DeliverByLog(DeliveryMethod):
    def __init__(self, config):
        """ just log that we tried to deliver. """
        import logging
        import sys
        self.logs = logging.getLogger(__name__)
        self.logs.setLevel(logging.DEBUG)
        log = logging.StreamHandler(sys.stdout)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log.setFormatter(formatter)
        self.logs.addHandler(log)

    def __call__(self, token, email):
        self.logs.debug("Deliver: " + token + " " + email)


# TODO: This needs to use Jinja2 templates
class DeliverBySMTP(DeliveryMethod):
    def __init__(self, config):
        """send by smtp"""
        import smtplib
        config = config['SMTP']
        self.servername = config.get('SERVER')
        self.template_path = config.get('TEMPLATE_PATH')
        self.from_email = config.get('FROM_EMAIL')
        self.msg_subject = config.get('MESSAGE_SUBJECT')
        self.server = smtplib.SMTP(self.servername)
        self.message_template = MessageTemplate(config)

    def __call__(self, token, toaddr):
        """send the login token"""
        from email.mime.text import MIMEText
        fromaddrs = self.from_email
        messagetext = self.message_template(token=token)
        msg = MIMEText(messagetext)
        msg['Subject'] = self.msg_subject  # TODO I think this should be a template string too?
        # msg['Subject'] = 'Login Token Request For %s' % toaddr
        msg['From'] = self.from_email
        msg['To'] = toaddr
        try:
            self.server.sendmail(fromaddrs, toaddr, msg.as_string())
            self.server.quit()
        except:
            print "You done goofed, can't send"


class DeliverByMandrill(DeliveryMethod):
    def __init__(self, config):
        import mandrill
        config = config['MANDRILL']
        self.mandrill = mandrill.Mandrill(config.get('API_KEY'))
        self.from_email = config.get('FROM')
        self.subject = config.get('SUBJECT')

    def __call__(self, login_url, email):
        message = dict(
            text="Here's your login url: {}".format(login_url),
            from_email=self.from_email,
            to=[{
                'email': email,
                'type': 'to',
                }],
            subject=self.subject,
        )
        try:
            self.mandrill.messages.send(message=message)
        except mandrill.Error as e:
            raise DeliveryError(str(e))


class DeliverByNull(DeliveryMethod):
    def __init__(self, config):
        pass

    def __call__(self, token, email):
        pass


DELIVERY_METHODS = {
    'mandrill': DeliverByMandrill,
    'smtp': DeliverBySMTP,
    'log': DeliverByLog,
    'null': DeliverByNull
}
