from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from .models import Note

NOTES_PER_PAGE = 10

def index(request):
  logged_in = request.user.is_authenticated

  page = int(request.GET.get('page', 0))
  notes_list = Note.objects.order_by("-update_time")[(page * NOTES_PER_PAGE):((page + 1) * NOTES_PER_PAGE)]
  context = {"notes_list": notes_list, "logged_in": logged_in}
  
  return render(request, "notes/index.html", context)

def login(request):
  if request.user.is_authenticated:
    return redirect('/')

  login_error = bool(request.GET.get('login_error', False))
  reg_error = bool(request.GET.get('reg_error', False))
  print(login_error, reg_error)
  context = {"reg_error": reg_error, "login_error": login_error}
  
  return render(request, "notes/login.html", context)

def logout(request):
  if not request.user.is_authenticated:
    return redirect('/')
  
  django_logout(request)
  return redirect('/')

def tryLogin(request):
  login = request.POST.get('login', '')
  password = request.POST.get('password', '')
  
  try:
    user = authenticate(request, username=login, password=password)
    django_login(request, user)

    return redirect('/')
  except:
    return redirect('/login?login_error=1')

def tryRegister(request):
  usr_login = request.POST.get('login', '')
  password = request.POST.get('password', '')

  try:
    user = User.objects.create_user(
      username=usr_login,
      password=password,
    )
    user.save()
    django_login(request, user)

    return redirect('/')
  except:
    return redirect('/login?reg_error=1')