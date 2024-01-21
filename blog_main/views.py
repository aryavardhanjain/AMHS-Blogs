from django.shortcuts import render, redirect
from blogs.models import Blog, Contact, Subscriber
from blogs.forms import ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from blogs.utils import send_subscription_email

def home(request):
    random_posts = Blog.objects.annotate(comment_count=Count('comment')).filter(status='Published').order_by('?')[:4]
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-updated_at')[:5]
    featured_posts = Blog.objects.annotate(comment_count=Count('comment')).filter(is_featured=True, status='Published').order_by('-updated_at')
    paginator = Paginator(featured_posts, 4)
    page_number = request.GET.get('page', 1)
    posts_page_obj = paginator.get_page(page_number)
    if request.method == 'POST' and 'subscribe' in request.POST:
        email = request.POST['email'].strip()
        if email:
            username = email.split('.')[0].split('@')[0]
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if created:
                mail_subject = 'Thank you for subscribing! '
                email_template = 'emails/subscription_email.html'
                context = {
                    'domain': request.get_host(),
                    'subscriber_email': subscriber.email,
                    'username': username.capitalize(),
                }
                
                email_response = send_subscription_email(subscriber.email, mail_subject, email_template, context)
                if email_response["success"]:
                    messages.success(request, 'Subscription successful! Check your email for confirmation. ')
                else:
                    messages.error(request, email_response["message"])
                return redirect(request.path)
            else:
                messages.info(request, 'You are already subscribed. ')
        else:
            messages.error(request, 'Please provide a valid email address. ')
        return redirect(request.path)

    context = {
        'posts_page_obj': posts_page_obj,
        'random_posts': random_posts,
        'posts': posts,
        'featured_posts': featured_posts,
        'current_page': 'home',
        'instagram_handle': 'Antarman: Mental Healthcare Services'
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('partials/posts_snippet.html', context)
        return HttpResponse(json.dumps({'html': html}), content_type="application/json")
    return render(request, 'home.html', context)

def about(request):
    context = {
        'current_page': 'about',
        'instagram_handle': 'Antarman: Mental Healthcare Services'
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact = Contact.objects.create(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Thank you for writing to us. ")
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'current_page': 'contact',
        'instagram_handle': 'Antarman: Mental Heathcare Services'
    }
    return render(request, 'contact.html', context)