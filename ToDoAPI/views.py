from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import Todo
# Create your views here.

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=email, email=email, password=password)
        
        return redirect('/login')
    
    
    return render(request, 'ToDoAPI/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=email, password=password)
        
        if user:
            login(request, user)
            
            return redirect('/welcome')
        
    return render(request, 'ToDoAPI/login.html')

@login_required
def welcome(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Todo.objects.create(user=request.user, title=title)
    
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ToDoAPI/welcome.html', {"todos" : todos})


def logout_view(request):
    logout(request)
    return redirect('/login')