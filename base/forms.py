from django.forms import ModelForm
from .models import Content, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
        exclude = ['host']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
