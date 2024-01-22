from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .utils import send_new_blog_email

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, full_name, password, **extra_fields):
        if not email:
            raise ValueError('The email field cannot be empty')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, full_name, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='caetgory_images/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    
    def published_blog_count(self):
        return self.blog_set.filter(status='Published').count()
    
STATUS_CHOICES = (
    ("Draft", "Draft"),
    ("Published", "Published"),
)
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    featured_image_1 = models.ImageField(upload_to='uploads/%Y/%m/%d')
    featured_image_2 = models.ImageField(upload_to='uploads/%Y/%m/%d')
    short_description = models.TextField(max_length=1000)
    introduction = models.TextField(max_length=1000)
    subheading_1 = models.TextField(max_length=100)
    para_1 = models.TextField(max_length=1500)
    subheading_2 = models.TextField(max_length=100)
    para_2 = models.TextField(max_length=1500)
    subheading_3 = models.TextField(max_length=100)
    para_3 = models.TextField(max_length=1500)
    subheading_4 = models.TextField(max_length=100)
    para_4 = models.TextField(max_length=1500)
    quote = models.CharField(max_length=250)
    quote_author = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding

        super().save(*args, **kwargs)

        if is_new and self.status == 'Published':
            send_new_blog_email(self)

class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    message = models.TextField(max_length=250, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_comments')

    def __str__(self):
        return f"Comment by {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email