from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("tryLogin", views.tryLogin, name="tryLogin"),
    path("tryRegister", views.tryRegister, name="tryRegister"),
    path("editNote", views.editNote, name="editNote"),
    path("saveNote", views.SaveNoteView.as_view(), name="saveNote"),
    path("deleteNote", views.DeleteNoteView.as_view(), name="deleteNote"),
    path("showNote/<int:note_id>", views.showNote, name="showNote"),
    path("topics", views.showTopics, name="topics"),
    path("editTopic", views.editTopic, name="editTopic"),
    path("saveTopic", views.SaveTopicView.as_view(), name="saveTopic"),
    path("deleteTopic", views.DeleteTopicView.as_view(), name="deleteTopic"),
]