from django.shortcuts import render, get_object_or_404
from .models import Snippet

# Create your views here.
def snippet_list(request):
    snippets = Snippet.created.all()
    return render(request, 'csnip/snippet/list.html', {'snippets':snippets})

def snippet_detail(request, year, month, day, snippet):
    snippet = get_object_or_404(Snippet, slug=snippet, created__year=year, created__month=month, created__day=day)
    return render(request, 'csnip/snippet/detail.html', {'snippet':snippet})    
