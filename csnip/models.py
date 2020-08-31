from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Snippet(models.Model):
    title = models.CharField(max_length = 30)
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ('-created',)

    def__str__(self):
    return self.title
