from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Content, Category, Message, User
from .forms import ContentForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')

    context = {'page':page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration failed')

    return render(request, 'base/login.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    contents = Content.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q) 
        )
                                      
    categories = Category.objects.all()[0:5]
    post_count = contents.count()
    comments = Message.objects.filter(Q(content__category__name__icontains=q))

    context = {'contents': contents, 'categories': categories, 'post_count': post_count,
               'comments':comments}
    return render(request, 'base/home.html', context)


def content(request, pk):
    content = Content.objects.get(id=pk)
    comments = content.message_set.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            content=content,
            body=request.POST.get('body')
        )
        return redirect('content', pk=content.id)
    
    context = {'content': content, 'comments':comments}
    return render(request, 'base/content.html', context)

@login_required(login_url='login')
def creatingContent(request):
    form = ContentForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        Content.objects.create(
            host=request.user,
            category=category,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
        
    context = {'form': form, 'categories': categories}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def updateContent(request, pk):
    content = Content.objects.get(id=pk)
    form = ContentForm(instance=content)
    categories = Category.objects.all()

    if request.user != content.host:
        return HttpResponse('You are not the host of this post')

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        content.name = request.POST.get('name')
        content.category = category
        content.description = request.POST.get('description')
        content.save()
        return redirect('home')

    context = {'form': form, 'categories': categories, 'content': content}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def deleteContent(request, pk):
    content = Content.objects.get(id=pk)

    if request.user != content.host :
        return HttpResponse('You are not the host of this post')
    
    if request.method == 'POST':
        content.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':content})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Message.objects.get(id=pk)

    if request.user != comment.user :
        return HttpResponse('You are not the host of this post')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': comment})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    contents = user.content_set.all()
    content_message = user.message_set.all()
    categories = Category.objects.all()
    context = {'user': user, 'contents': contents, 'content_post': content_message, 'categories': categories}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def categoriesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.filter(name__icontains=q)
    return render(request, 'base/categories.html', {'categories': categories})

def recentPost(request):
    content_comment = Message.objects.all()
    return render(request, 'base/recent_post.html', {'content_comment': content_comment})