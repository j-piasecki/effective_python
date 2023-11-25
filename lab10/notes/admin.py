from django.contrib import admin

from .models import Note, Topic

admin.site.register(Note)
admin.site.register(Topic)
