"""
URL configuration for blog_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as BlogsView
from allauth.socialaccount import urls as socialaccount_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blogs/search/', BlogsView.search, name='search'),
    path('blogs/<slug:slug>/', BlogsView.blogs, name='blogs'),
    path('blogs/like_comment/<int:comment_id>/', BlogsView.like_comment, name='like_comment'),
    path('register/', BlogsView.register, name='register'),
    path('login/', BlogsView.login, name='login'),
    path('logout/', BlogsView.logout, name='logout'),
    path('category/', include('blogs.urls')),
    path('accounts/', include('allauth.urls')),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    # path('blogs/', include('blogs.urls')),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
