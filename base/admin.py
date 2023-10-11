from django.contrib import admin

# Register your models here.

from .models import Content, Message, Category, User


admin.site.register(Content)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(User)