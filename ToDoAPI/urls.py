from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login_view, name='login'),
    path('welcome', views.welcome),
    path('logout', views.logout_view, name='logout'),
    path('toggle/<int:todo_id>', views.toggle_todo, name='toggle'),
    path('delete/<int:todo_id>', views.delete_task, name='delete'),
]