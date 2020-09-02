from django.contrib import admin
from .models import Snippet

# admin.site.register(Snippet)
@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','created')
    list_filter = ('created','title','author')
    search_fields = ('body',)
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('created','title')
