from django.shortcuts import render, get_object_or_404, redirect
from .models import Snippet, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

from django.views.generic import ListView
from .forms import SnippetCreateForm, EmailPostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
import uuid
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag
from django.db.models import Count


# uuid.uuid4().hex[:6].upper()


# Create your views here.

def snippet_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Snippet.publishedd.annotate(search=SearchVector('title','body'),).filter(search=query)

    return render(request, 'csnip/snippet/search.html', {'form':form, 'query':query, 'results':results})






# class SnippetListView(ListView):
#     queryset = Snippet.published.all()
#     context_object_name = 'snippets'
#     paginate_by = 5
#     template_name = 'csnip/snippet/list.html'
def snippet_share(request, snippet_id):
    # Retrieve snippet by id
    snippet = get_object_or_404(Snippet, id=snippet_id)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            snippet_url = request.build_absolute_uri(snippet.get_absoulte_url())
            subject = '{} ({}) wants to share snippet "{}"'.format(cd['name'], cd['email'], snippet.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(snippet.title, snippet_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@csnip.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'csnip/snippet/share.html',{'snippet':snippet, 'form':form, 'sent':sent})



def snippet_list(request, tag_slug=None):
    object_list = Snippet.publishedd.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list,3)
    page = request.GET.get('page')
    try:
        snippets = paginator.page(page)
    except PageNotAnInteger:
        snippets = paginator.page(1)
    except EmptyPage:
        snippets = paginator.page(paginator.num_pages)

    return render(request, 'csnip/snippet/list.html', {'page':page,'snippets':snippets, 'tag':tag})


def snippet_detail(request, year, month, day, snippet):
    snippet = get_object_or_404(Snippet, slug=snippet)
    # , created__year=year, created__month=month, created__day=day)
    # List of active comments for this snippet
    comments = snippet.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.snippet = snippet
            new_comment.save()
    else:
        comment_form = CommentForm()


    # List of similar snippets
    snippet_tags_ids = snippet.tags.values_list('id', flat=True)
    similar_snippets = Snippet.publishedd.filter(tags__in=snippet_tags_ids).exclude(id=snippet.id)
    similar_snippets = similar_snippets.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:4]
    return render(request, 'csnip/snippet/detail.html', {'snippet':snippet,'comments':comments, 'new_comment':new_comment,'comment_form':comment_form, 'similar_snippets':similar_snippets})





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
            s = new_item.title[::-1]+new_item.explanation[:5]+uuid.uuid4().hex[:6].upper()
            new_item.slug = slugify(s)
            # assign current user to the snippet
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Snippet Added Successfully")

            # redirect to newly created item detail view
            # try:
            return redirect(new_item.get_absoulte_url())
            # except:



    else:
        form = SnippetCreateForm()

    return render(request, 'csnip/snippet/create.html',{'section':'snippet', 'form':form})
