from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib import messages
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    return redirect('login')

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
        deadline = request.POST.get("deadline")
        if not deadline:
            deadline = None
        if title:
            Todo.objects.create(user=request.user, title=title, deadline=deadline)
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
        new_deadline = request.POST.get('new_deadline')
        if new_todo:
            todo.title = new_todo
        if new_deadline:
            todo.deadline = new_deadline
        if 'remove_deadline' in request.POST:
            todo.deadline = None
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

@login_required
def profile(request):
    return render(request, 'ToDoAPI/profile.html')

@login_required
def change(request):
    user = get_object_or_404(User, username=request.user.username)
    edit = request.GET.get('edit')
    if 'update_user_info' in request.POST:
        new_username = request.POST.get('new_username').strip()
        new_email = request.POST.get('new_email').strip()
        if new_username and new_email:  
            if User.objects.filter(username=new_username).exists() and new_username!=request.user.username:
                messages.error(request, "This username already used")
            elif User.objects.filter(email=new_email).exists() and new_email!=request.user.email:
                messages.error(request, "This email already registered")
            else:
                user.username = new_username
                user.email = new_email
                user.save()
                messages.success(request, "Changes saved successfully")
                return redirect('/profile')
            
    elif 'update_password' in request.POST:
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password').strip()
        re_new_password = request.POST.get('re_new_password').strip()
        if not user.check_password(old_password):
            messages.error(request, "Password is wrong")
        else:
            if new_password and re_new_password:
                if new_password != re_new_password:
                    messages.error(request, "Doesn't match new password")
                else:
                    user.set_password(new_password)
                    user.save()
                    
                    update_session_auth_hash(request, user)
                    messages.success(request, "Changes saved successfully")
                    return redirect('/profile')
    return render(request, 'ToDoAPI/profile.html', {"mode" : edit})