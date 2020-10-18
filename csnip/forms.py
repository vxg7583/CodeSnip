from urllib import request
from django.core.files.base import ContentFile
from django import forms
from .models import Snippet, Comment
from django.utils.text import slugify
from taggit.forms import *

class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('title','body','explanation','tags')
        widgets = { 'title': forms.TextInput(attrs={'size': 100})}

        # widget=forms.TextInput(attrs={'size':'30','maxlength':'100'})


    # def save(self, force_insert=False, force_update=False, commit=True):
    #     snippet = super(SnippetCreateForm, self).save(commit=False)
    #     snippet.snippet.save(snippet, save = False)
    #
    #     if commit:
    #         snippet.save()
    #
    #     return snippet

class SnippetEditForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('title','body','explanation','tags')
        widgets = { 'title': forms.TextInput(attrs={'size': 100})}

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')





class SearchForm(forms.Form):

        query = forms.CharField(label=' ')
