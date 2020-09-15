from urllib import request
from django.core.files.base import ContentFile
from django import forms
from .models import Snippet
from django.utils.text import slugify

class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('title','body','explanation')

    # def save(self, force_insert=False, force_update=False, commit=True):
    #     snippet = super(SnippetCreateForm, self).save(commit=False)
    #     snippet.snippet.save(snippet, save = False)
    #
    #     if commit:
    #         snippet.save()
    #
    #     return snippet
