from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

class Note(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True, blank=True)

class Topic(TimeStampedModel, TitleSlugDescriptionModel):
    public = models.BooleanField(default=False)
    subtopic_of = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
