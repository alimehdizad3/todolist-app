from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login_view, name='login'),
    path('welcome', views.welcome),
    path('logout', views.logout_view, name='logout')
]