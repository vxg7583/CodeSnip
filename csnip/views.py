from django.shortcuts import render, get_object_or_404, redirect
from .models import Snippet
from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

from django.views.generic import ListView
from .forms import SnippetCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify


# Create your views here.
# class SnippetListView(ListView):
#     queryset = Snippet.published.all()
#     context_object_name = 'snippets'
#     paginate_by = 5
#     template_name = 'csnip/snippet/list.html'

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

@login_required
def snippet_create(request):
    '''
    user uploads a new snippet which is saved to the database
    '''
    if request.method == 'POST':
        # form is sent
        form = SnippetCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the snippet
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Snippet Added Successfully")

            # redirect to newly created item detail view
            return redirect(new_item.get_absoulte_url())
    else:
        form = SnippetCreateForm()

    return render(request, 'csnip/snippet/create.html',{'section':'snippet', 'form':form})
