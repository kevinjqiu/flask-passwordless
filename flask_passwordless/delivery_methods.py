import abc
import logging
import sys
try:
    import mandrill
except ImportError:
    pass
from templates import MessageTemplate
import smtplib


class DeliveryMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, login_url, **kwargs):
        return


class DeliveryError(StandardError):
    pass


class DeliverByNull(DeliveryMethod):
    def __init__(self, config):
        pass

    def __call__(self, token, email):
        pass


class DeliverByLog(DeliveryMethod):
    def __init__(self, config):
        """ just log that we tried to deliver. """
        self.logs = logging.getLogger(__name__)
        self.logs.setLevel(logging.DEBUG)
        log = logging.StreamHandler(sys.stdout)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log.setFormatter(formatter)
        self.logs.addHandler(log)

    def __call__(self, token, email):
        self.logs.debug("Deliver: " + token + " " + email)


class DeliverByMandrill(DeliveryMethod):
    def __init__(self, config):
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

# TODO: This needs to use Jinja2 templates
class DeliverBySMTP(DeliveryMethod):
    def __init__(self, config):
        """send by smtp"""
        self.tmpl_config = config['TEMPLATES']
        self.config = config['SMTP']
        self.from_email = self.config.get('FROM_EMAIL')
        self.msg_subject = self.config.get('MESSAGE_SUBJECT')
        self.server = smtplib.SMTP(self.config.get('SERVER'))
        self.message_template = MessageTemplate(self.tmpl_config)

    def __call__(self, token, email):
        """send the login token"""
        from email.mime.text import MIMEText
        fromaddrs = self.from_email
        messagetext = self.message_template(token=token)
        target_email = email + '@' + self.config.get('OK_DOMAIN')
        msg = MIMEText(messagetext, 'html')
        msg['Subject'] = self.msg_subject
        msg['From'] = self.from_email
        msg['To'] = target_email
        try:
            self.server.sendmail(fromaddrs, target_email, msg.as_string())
            self.server.quit()
        except:
            print "You done goofed, can't send"


DELIVERY_METHODS = {
    'mandrill': DeliverByMandrill,
    'smtp': DeliverBySMTP,
    'log': DeliverByLog,
    'null': DeliverByNull
}
