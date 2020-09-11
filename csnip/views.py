from django.shortcuts import render, get_object_or_404
from .models import Snippet
from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

from django.views.generic import ListView


# Create your views here.
def snippet_list(request):
    object_list = Snippet.published.all()
    paginator = Paginator(object_list,3)
    page = request.GET.get('page')
    try:
        snippets = paginator.page(page)
    except PageNotAnInteger:
        snippets = paginator.page(1)
    except EmptyPage:
        snippets = paginator.page(paginator.num_pages)

    return render(request, 'csnip/snippet/list.html', {'page':page,'snippets':snippets})

def snippet_detail(request, year, month, day, snippet):
    snippet = get_object_or_404(Snippet, slug=snippet, created__year=year, created__month=month, created__day=day)
    return render(request, 'csnip/snippet/detail.html', {'snippet':snippet})

# class SnippetListView(ListView):
#     queryset = Snippet.published.all()
#     context_object_name = 'snippets'
#     paginate_by = 5
#     template_name = 'csnip/snippet/list.html'
