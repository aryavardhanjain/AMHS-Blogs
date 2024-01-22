from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Category, Comment, CustomUser, Subscriber
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .forms import CommentForm, UserRegistrationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .utils import send_subscription_email

# Create your views here.
def posts_by_category(request, category_id):
    recent_posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-updated_at')[:5]
    all_posts = Blog.objects.filter(category_id=category_id, status='Published')

    for post in all_posts:
        post.comment_count = Comment.objects.filter(post=post).count()    

    paginator = Paginator(all_posts, 7)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    
    category = get_object_or_404(Category, id=category_id)

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
                if email_response['success']:
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
        'recent_posts': recent_posts,
        'posts': posts,
        'category': category,
        'instagram_handle': 'Antarman: Mental Healthcare Services'
    }
    return render(request, 'posts_by_category.html', context)

def search(request):
    keyword = request.GET['keyword']
    all_blogs = Blog.objects.annotate(comment_count=Count('comment')).filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(introduction__icontains=keyword) | Q(para_1__icontains=keyword) | Q(para_2__icontains=keyword) | Q(para_3__icontains=keyword) | Q(para_4__icontains=keyword) | Q(quote__icontains=keyword) | Q(quote_author__icontains=keyword) | Q(subheading_1__icontains=keyword) | Q(subheading_2__icontains=keyword) | Q(subheading_3__icontains=keyword) | Q(subheading_4__icontains=keyword), status='Published')
    
    paginator = Paginator(all_blogs, 7)
    page_number = request.GET.get('page', 1)
    blogs = paginator.get_page(page_number)
    
    context = {
        'blogs':blogs,
        'keyword':keyword,
        'instagram_handle': 'Antarman: Mental Healthcare Services'
    }
    return render(request, 'search.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    previous_post = Blog.objects.filter(created_at__lt=single_blog.created_at, status='Published').order_by('-created_at').first()
    next_post = Blog.objects.filter(created_at__gt=single_blog.created_at, status='Published').order_by('created_at').first()
    comments = Comment.objects.filter(post = single_blog)
    comment_count = comments.count()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = single_blog
            comment.save()
            return JsonResponse({'status': 'success', 'comment_id': comment.id, 'comment_name': comment.name, 'comment_date': comment.created_at.strftime('%d %b %Y'), 'comment_message': comment.message})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    form = CommentForm()
    context = {
        'previous_post': previous_post,
        'next_post': next_post,
        'comment_count': comment_count,
        'comments': comments,
        'single_blog': single_blog,
        'form': form,
        'instagram_handle': 'Antarman: Mental Healthcare Services'
    }
    return render(request, 'blogs.html', context)

@login_required
@require_POST
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': comment.likes.count()})

def register(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = CustomUser.objects.create_user(username=username, full_name=full_name, email=email, password=password)
            user.save()
            return HttpResponseRedirect(next_url)
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'active_tab': 'register',
        'next': next_url,
    }
    return render(request, 'signin.html', context)

def login(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, "Invalid Login Credentials. Please try again! ")
            return render(request, 'signin.html', {'active_tab': 'login'})
    context = {
        'next': next_url,
        'active_tab': 'login',
    }
    return render(request, 'signin.html', context)

def logout(request):
    next_url = request.GET.get('next', '/')
    auth.logout(request)
    return HttpResponseRedirect(next_url)
