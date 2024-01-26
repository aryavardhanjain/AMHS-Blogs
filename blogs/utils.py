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
    
def send_new_blog_email(blog, request=None):
    from .models import Subscriber

    subscribers = Subscriber.objects.all()
    mail_subject = f"New Blog Posted: {blog.title}"
    email_template = 'emails/new_blog_notification.html'

    local_domain = 'http://127.0.0.1:8000'
    
    results = []
    for subscriber in subscribers:
        try:
            image_url = None
            if blog.featured_image_1:
                image_url = local_domain + blog.featured_image_1.url
            context = {
                'domain': local_domain,
                'blog': blog,
                'subscriber': subscriber,
                'image_url': image_url
            }
            print("Sending email with image URL: ", image_url)
            message = render_to_string(email_template, context)
            mail = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            mail.content_subtype = 'html'
            mail.send()
            results.append({'email': subscriber.email, 'status': 'sent'})
        except SMTPException as e:
            results.append({'email': subscriber.email, 'status': f'failed: {str(e)}'})
    return results