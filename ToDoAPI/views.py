from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username already used')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'This email already registered')
            return redirect('/register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
        
        return redirect('/login')
    
    
    return render(request, 'ToDoAPI/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            
            return redirect('/welcome')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/login')
    return render(request, 'ToDoAPI/login.html')

@login_required
def welcome(request):
    if request.method == "POST":
        title = request.POST.get("title")
        title = title.strip()
        if title:
            Todo.objects.create(user=request.user, title=title)
        return redirect('/welcome')
    
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    search = request.GET.get("search")
    if search:
        search = search.strip()
        todos = todos.filter(title__icontains=search)
    else:
        search=""
    
    filter_type = request.GET.get("filter", "")
    if filter_type:
        if filter_type == "pending":
            todos = todos.filter(completed=False)
        elif filter_type == "completed":
            todos = todos.filter(completed=True)

    total = todos.count()
    c_count = todos.filter(completed=True).count()
    u_count = todos.filter(completed=False).count()
    return render(request, 'ToDoAPI/welcome.html', {"todos" : todos, "total" : total, "completed" : c_count, "uncompleted" : u_count, "search" : search, "filter_type" : filter_type})


def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required
def toggle_todo(request, todo_id):
    if request.method=="POST":
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
    next_url = request.POST.get("next", "/welcome")
    return redirect(next_url)

@login_required
def delete_task(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.delete()
    next_url = request.POST.get("next", "/welcome")
    return redirect(next_url)

@login_required
def edit_task(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        new_todo = request.POST.get('new_todo').strip()
        if new_todo:
            todo.title = new_todo
            todo.save()
        next_url = request.POST.get("next", "/welcome")
        return redirect(next_url)
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    search = request.GET.get("search", "")
    if search:
        todos = todos.filter(title__icontains=search)
    filter_type = request.GET.get("filter", "")
    if filter_type:
        if filter_type == "pending":
            todos = todos.filter(completed=False)
        elif filter_type == "completed":
            todos = todos.filter(completed=True)
    return render(request, 'ToDoAPI/welcome.html', {"todos" : todos, "editing_id" : todo_id, "search" : search, "filter_type" : filter_type})