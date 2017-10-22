from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from django.conf import settings
from customer.models import Customer


def send_verification_mail(email_verify_data):
    encoded_data = signing.dumps(email_verify_data)
    verification_link = settings.VERSIONED_BASE_URL[
        'v1'] + 'customer/verify_email/' + encoded_data
    template = get_template('messenger/v1/email_verify.html')
    html_part = template.render({'verification_link': verification_link})
    msg = EmailMultiAlternatives('Email verification Link, Startup Name',
                                 None, settings.SENDER_EMAIL, [email_verify_data['email_id']])
    msg.attach_alternative(html_part, 'text/html')
    msg.send(True)
