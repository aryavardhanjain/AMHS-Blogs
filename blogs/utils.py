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
        return {'success': True, 'message': 'Email sent successfully. '}
    except SMTPException as e:
        return {'success': False, 'message': f'Error sending email: {str(e)}'}
    
def send_new_blog_email(blog):
    from .models import Subscriber

    subscribers = Subscriber.objects.all()
    mail_subject = f"New Blog Posted: {blog.title}"
    email_template = 'emails/new_blog_notification.html'
    results = []
    
    for subscriber in subscribers:
        try:
            context = {
                'blog': blog,
                'subscriber': subscriber,
                'image_url': blog.featured_image_1.url if blog.featured_image_1 else None
            }
            message = render_to_string(email_template, context)
            mail = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            mail.content_subtype = 'html'
            mail.send()
            results.append({'email': subscriber.email, 'status': 'sent'})
        except SMTPException as e:
            results.append({'email': subscriber.email, 'status': f'failed: {str(e)}'})
    return results