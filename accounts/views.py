from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib.auth.models import User


# Create your views here.
@csrf_exempt
def index_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        return render(request, "accounts/index.html")


@csrf_exempt
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                message = messages.success(request, f"Account created")
                return redirect("/login/")
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
            else:
                messages.error(request, "Username or password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="login")
@csrf_exempt
def home(request):
    todo_items = Todo.objects.filter(object_id=request.user.id).order_by('-added_date')
    print(todo_items)
    return render(request, 'accounts/home.html', {"todo_items": todo_items})


@csrf_exempt
def add_todo(request):
    current_date = timezone.now()
    content = request.POST["content"]
    if content != "":
        message = messages.success(request, "item added")
        user = User.objects.get(username=request.user.username)
        todo = Todo(content_object=user, text=content, added_date=current_date)
        todo.save()
    return HttpResponseRedirect("/home/")


@csrf_exempt
def delete_todo(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    message = messages.success(request, "item deleted")
    return HttpResponseRedirect("/home/")
