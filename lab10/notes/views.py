from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View

from .models import Note, Topic

NOTES_PER_PAGE = 10

def index(request):
  logged_in = request.user.is_authenticated

  page = int(request.GET.get('page', 0))
  topic = request.GET.get('topic', None)

  if topic:
    notes_list = Note.objects.filter(topic=topic).order_by("-modified")[(page * NOTES_PER_PAGE):((page + 1) * NOTES_PER_PAGE)]
  else:
    notes_list = Note.objects.order_by("-modified")[(page * NOTES_PER_PAGE):((page + 1) * NOTES_PER_PAGE)]
  
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

def editNote(request):
  if not request.user.is_authenticated:
    return redirect('/login')

  title = ''
  content = ''
  topic = None

  note_id = request.GET.get('id', None)

  try:
    note = Note.objects.get(id=note_id)
  except:
    note = None

  if note:
    title = note.title
    content = note.content
    topic = note.topic

  if topic:
    topic_id = topic.id
  else:
    topic_id = None

  topics = Topic.objects.order_by("-title")
  context = {"title": title, "content": content, "topic_id": topic_id, "note_id": note_id, "topics": topics}
  
  return render(request, "notes/editNote.html", context)

class SaveNoteView(UserPassesTestMixin, View):
  def post(self, request):
    note_id = self.request.POST.get('note_id', None)
    if note_id == 'None':
      note_id = None

    title = self.request.POST.get('title', '')
    content = self.request.POST.get('content', '')
    topic_id = self.request.POST.get('topic', None)

    if note_id:
      note = Note.objects.get(id=note_id)
      note.title = title
      note.content = content
      note.topic = Topic.objects.get(id=topic_id)
      note.save()
    else:
      note = Note.objects.create(
        title=title,
        content=content,
        created_by=request.user,
        topic=Topic.objects.get(id=topic_id),
      )
      note.save()

    return redirect('/')

  def test_func(self):
    if not self.request.user.is_authenticated:
      return False

    try:
      note_id = self.request.POST.get('note_id', None)
      note = Note.objects.get(id=note_id)
      return note.created_by == self.request.user
    except:
      return True

class DeleteNoteView(UserPassesTestMixin, View):
  def get(self, request):
    note_id = self.request.GET.get('note_id', None)

    note = Note.objects.get(id=note_id)
    note.delete()

    return redirect('/')

  def test_func(self):
    if not self.request.user.is_authenticated:
      return False

    if self.request.user.is_superuser:
      return True

    try:
      note_id = self.request.POST.get('note_id', None)
      note = Note.objects.get(id=note_id)
      return note.created_by == self.request.user
    except:
      return False

def showNote(request, note_id):
  try:
    note = Note.objects.get(id=note_id)
  except:
    return HttpResponseNotFound("Note doesn't exist")

  title = note.title
  content = note.content
  topic = note.topic
  author = note.created_by

  can_delete = note.created_by == request.user or request.user.is_superuser
  can_edit = note.created_by == request.user

  context = {"title": title, "content": content, "topic": topic, "author": author, "note_id": note_id, "can_delete": can_delete, "can_edit": can_edit }
  
  return render(request, "notes/showNote.html", context)

def showTopics(request):
  topics = Topic.objects.order_by("-title")

  context = {"topics": topics, "can_edit": request.user.is_superuser, "logged_in": request.user.is_authenticated}
  
  return render(request, "notes/topics.html", context)

def editTopic(request):
  if not request.user.is_superuser:
    return redirect('/login')

  title = ''
  description = ''
  parent = None

  topic_id = request.GET.get('id', None)

  try:
    topic = Topic.objects.get(id=topic_id)
  except:
    topic = None

  if topic:
    title = topic.title
    description = topic.description
    parent = topic.subtopic_of

  if parent:
    parent_id = parent.id
  else:
    parent_id = None

  topics = Topic.objects.order_by("-title")
  context = {"title": title, "description": description, "parent_id": parent_id, "topic_id": topic_id, "topics": topics}
  
  return render(request, "notes/editTopic.html", context)

class SaveTopicView(UserPassesTestMixin, View):
  def post(self, request):
    topic_id = self.request.POST.get('topic_id', None)
    if topic_id == 'None':
      topic_id = None

    title = self.request.POST.get('title', '')
    description = self.request.POST.get('description', '')
    parent_id = self.request.POST.get('parent', None)

    if topic_id:
      topic = Topic.objects.get(id=topic_id)
      topic.title = title
      topic.description = description
      topic.parent = Topic.objects.get(id=parent_id)
      topic.save()
    else:
      topic = Topic.objects.create(
        title=title,
        description=description,
        subtopic_of=Topic.objects.get(id=parent_id),
      )
      topic.save()

    return redirect('/topics')

  def test_func(self):
    topic_id = self.request.POST.get('topic_id', None)
    if topic_id == 'None':
      topic_id = None

    return self.request.user.is_superuser and (topic_id is None or int(topic_id) > 1)

class DeleteTopicView(UserPassesTestMixin, View):
  def get(self, request):
    topic_id = self.request.GET.get('id', None)

    topic = Topic.objects.get(id=topic_id)
    topic.delete()

    return redirect('/topics')

  def test_func(self):
    topic_id = self.request.POST.get('topic_id', None)
    if topic_id == 'None':
      topic_id = None

    return self.request.user.is_superuser and (topic_id is None or int(topic_id) > 1)
