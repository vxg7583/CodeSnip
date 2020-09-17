from django.contrib import admin
from .models import Snippet, Comment

# admin.site.register(Snippet)
@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','created')
    list_filter = ('created','title','author')
    search_fields = ('title','author', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','snippet','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name', 'email','body')
