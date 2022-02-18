from cgitb import html
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Token Related
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token


def send_mail(request, subscriber, html_content=None, subject=None):

    email = subscriber.email

    token = account_activation_token.make_token(subscriber)
    current_site = get_current_site(request)

    if html_content is None:
        html_content = render_to_string('blog/email/sub_conf.html', {
            'user': subscriber,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(subscriber.pk)),
            'token': token,
        })

    if subject is None:
        subject = 'Subscription Confirmation for Sean Stocker\'s Blog'

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False
