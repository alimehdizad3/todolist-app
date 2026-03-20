from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Todo
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

@login_required
def toggle_todo(request, todo_id):
    if request.method=="POST":
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
    return redirect('/welcome')

@login_required
def delete_task(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.delete()
    return redirect('/welcome')