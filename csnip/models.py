from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Snippet(models.Model):
    title = models.TextField(max_length = 30)
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=300, unique_for_date='created')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets_posts', default="NONAME")

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
