from django.urls import path
from . import views

app_name = 'csnip'
# REMEMBER THAT A URL PATH CONSISTS OF A STRING PATTERN, A VIEW AND A OPTIONAL NAME THAT ALLOWS YOU TO NAME THE URL SITE WIDE
urlpatterns = [

    # snippet views
    path('',views.snippet_list, name='snippet_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:snippet>/',\
         views.snippet_detail, name='snippet_detail'),


]
