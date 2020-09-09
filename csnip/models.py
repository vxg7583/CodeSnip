from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class SnippetManager(models.Manager):
    def get_queryset(self):
        return super(SnippetManager, self).get_queryset().filter(author=1)








class Snippet(models.Model):
    title = models.TextField(max_length = 30)
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=300, unique_for_date='created')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets_posts', default="NONAME")
    published = SnippetManager()
    explanation = models.TextField(max_length=500, default='NO EXPLANATION')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absoulte_url(self):
        return reverse('csnip:snippet_detail', args=[self.created.year, \
                                                    self.created.month,\
                                                    self.created.day,
                                                    self.slug])
