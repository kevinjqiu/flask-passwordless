import abc
import logging
import sys
try:
    import mandrill
except ImportError:
    pass
from templates import MessageTemplate
import smtplib
from email.mime.text import MIMEText


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


class DeliverBySMTP(DeliveryMethod):
    def __init__(self, config):
        """send by smtp"""
        self.tmpl_config = config['TEMPLATES']
        self.config = config['SMTP']

    def __call__(self, token, email):
        """send the login token"""
        self.from_email = self.config.get('FROM_EMAIL')
        self.msg_subject = self.config.get('MESSAGE_SUBJECT')
        self.server = smtplib.SMTP()
        self.message_template = MessageTemplate(self.tmpl_config)
        fromaddrs = self.from_email
        messagetext = self.message_template(token=token)
        target_email = email + '@' + self.config.get('OK_DOMAIN')
        msg = MIMEText(messagetext, 'html')
        msg['Subject'] = self.msg_subject
        msg['From'] = self.from_email
        msg['To'] = target_email
        try:
            self.server.connect(self.config.get('SERVER'))
            self.server.sendmail(fromaddrs, target_email, msg.as_string())
            self.server.quit()
        except smtplib.SMTPRecipientsRefused as e:
            print "recipients refused"
            print e
        except smtplib.SMTPException as aa:
            print "generic exception"
            print aa
        except smtplib.SMTPDataError as de:
            print "data error"
            print de
        except smtplib.SMTPConnectError as ce:
            print "connect error"
            print ce
        except:
            print "wat"


DELIVERY_METHODS = {
    'mandrill': DeliverByMandrill,
    'smtp': DeliverBySMTP,
    'log': DeliverByLog,
    'null': DeliverByNull
}
