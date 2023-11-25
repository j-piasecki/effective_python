from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    update_time = models.DateTimeField("last update time")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
