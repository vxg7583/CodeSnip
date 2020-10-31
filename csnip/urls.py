from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'csnip'
# REMEMBER THAT A URL PATH CONSISTS OF A STRING PATTERN, A VIEW AND A OPTIONAL NAME THAT ALLOWS YOU TO NAME THE URL SITE WIDE
urlpatterns = [

    # snippet views
    path('',views.snippet_list, name='snippet_list'),
    path('tag/<slug:tag_slug>/', views.snippet_list, name='snippet_list_by_tag'),


    path('<int:year>/<int:month>/<int:day>/<slug:snippet>/',\
         views.snippet_detail, name='snippet_detail'),
    path('create/', views.snippet_create, name='create'),
    path('<int:snippet_id>/share/', views.snippet_share, name = 'snippet_share'),
    path('search/', views.snippet_search, name='snippet_search'),
    # path('search1/', include('haystack.urls'), name='snippet_search1'),
    path('like/', views.snip_like, name='like'),
    path('delete/<int:snippet_id>', views.snippet_delete, name='delete'),
    path('edit/<int:pk>/', views.snippet_edit, name='edit'),
    path('delete_comment/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('about/', TemplateView.as_view(template_name="csnip/snippet/about.html"), name='csnip-about'),



]
