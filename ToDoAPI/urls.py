from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('welcome', views.welcome, name='welcome'),
    path('logout', views.logout_view, name='logout'),
    path('toggle/<int:todo_id>', views.toggle_todo, name='toggle'),
    path('delete/<int:todo_id>', views.delete_task, name='delete'),
    path('edit/<int:todo_id>', views.edit_task, name='edit'),
    path('profile', views.profile, name='profile'),
    path('change', views.change, name='change'),
]