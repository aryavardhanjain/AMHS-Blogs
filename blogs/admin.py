from django.contrib import admin
from .models import Category, Blog, Contact, Comment, CustomUser, Subscriber
from django.contrib.auth.admin import UserAdmin


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'image')
    list_editable = ('image', )

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    list_display = ('email', 'full_name', 'username', 'is_active')
    ordering = ('-date_joined',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscriber)