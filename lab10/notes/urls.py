from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("tryLogin", views.tryLogin, name="tryLogin"),
    path("tryRegister", views.tryRegister, name="tryRegister"),
]