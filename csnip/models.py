from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# Create your models here.


class SnippetManager(models.Manager):

    def get_queryset(self):
        return super(SnippetManager, self).get_queryset().filter()


class Snippet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='snippets_created', on_delete=models.CASCADE)
    title = models.CharField(max_length = 200, verbose_name="")
    body = RichTextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.CharField(user, max_length=500)
    publishedd = SnippetManager()
    explanation = RichTextField()
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='snippets_liked',blank=True)
    tags = TaggableManager()
    title_vector = SearchVectorField(null=True)
    explanation_vector = SearchVectorField(null=True)
    # comments_vector = SearchVectorField(null=True)
    # author_vector = SearchVectorField(null=True)



    class Meta:
        indexes = [GinIndex(fields=["title_vector", "explanation_vector"])]
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('csnip:snippet_detail', args=[self.created.year, \
                                                    self.created.month,\
                                                    self.created.day,self.slug])


    def __str__(self):
        return self.title




class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_created', null=True)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.snippet)
