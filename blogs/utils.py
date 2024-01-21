from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException

def send_subscription_email(email, mail_subject, email_template, context):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        message = render_to_string(email_template, context)
        mail = EmailMessage(mail_subject, message, from_email, to=[email])
        mail.content_subtype = 'html'
        mail.send()
        return {'success': True, 'message': 'Email sen successfully. '}
    except SMTPException as e:
        return {'success': False, 'message': f'Error sending email: {str(e)}'}