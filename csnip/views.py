from django.shortcuts import render, get_object_or_404, redirect
from .models import Snippet, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

from django.views.generic import ListView
from .forms import SnippetCreateForm, EmailPostForm, CommentForm, SearchForm, SnippetEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
import uuid
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.postgres.search import TrigramSimilarity
# from django_comments.views.moderation import perform_delete
# from django_comments.models import Comment
import django.http as http
from actions.utils import create_action
# uuid.uuid4().hex[:6].upper()


# Create your views here.

def snippet_search(request):
    form = SearchForm()
    query = None
    results = []
    # page = None



    if 'query' in request.GET:
        # page = request.GET.get('page',1)
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']

            results = Snippet.publishedd.annotate(
                rank=SearchRank(
                    'title_vector',
                    SearchQuery(query, config="english")
                )

            ).annotate(
                rank=SearchRank(
                    'explanation_vector',
                    SearchQuery(query, config="english")
                )
                # similarity=TrigramSimilarity(F('explanation_vector'), query)
            ).filter(rank__gte=0.00000000001).order_by('-rank')

            # results = results.filter(rank__gte=0.00001).order_by('-rank')
            # results = Snippet.publishedd.filter(Q(title_vector__icontains=query) \
            # | Q(explanation_vector__icontains=query))

    #     paginator = Paginator(results, 4)
    #
    # #
    #     try:
    #         results = paginator.page(page)
    #     except PageNotAnInteger:
    #         results = paginator.page(1)
    #     except EmptyPage:
    #         results = paginator.page(paginator.num_pages)


    return render(request, 'csnip/snippet/search.html', {'form':form, 'query':query, 'results':results})

    # else:
    #     return render(request, 'csnip/snippet/search.html', {'form':form, 'query':query, 'results':results})
    #









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
            snippet_url = request.build_absolute_uri(snippet.get_absolute_url())
            subject = '{} ({}) wants to share snippet "{}"'.format(cd['name'], cd['email'], snippet.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(snippet.title, snippet_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@codesnips.org', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'csnip/snippet/share.html',{'snippet':snippet, 'form':form, 'sent':sent})



def snippet_list(request, tag_slug=None):
    search_form = SearchForm()
    object_list = Snippet.publishedd.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list,10)
    page = request.GET.get('page')
    try:
        snippets = paginator.page(page)
    except PageNotAnInteger:
        snippets = paginator.page(1)
    except EmptyPage:
        snippets = paginator.page(paginator.num_pages)

    return render(request, 'csnip/snippet/list.html', {'search_form':search_form, 'page':page,'snippets':snippets, 'tag':tag})


def snippet_detail(request, year, month, day, snippet):
    snippet = get_object_or_404(Snippet, slug=snippet)
    user = request.user
    # , created__year=year, created__month=month, created__day=day)
    # List of active comments for this snippet
    comments = snippet.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.snippet = snippet
            new_comment.save()
    else:
        comment_form = CommentForm()


    # List of similar snippets
    snippet_tags_ids = snippet.tags.values_list('id', flat=True)
    similar_snippets = Snippet.publishedd.filter(tags__in=snippet_tags_ids).exclude(id=snippet.id)
    similar_snippets = similar_snippets.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:5]
    return render(request, 'csnip/snippet/detail.html', {'snippet':snippet,'comments':comments, 'new_comment':new_comment,'comment_form':comment_form, 'similar_snippets':similar_snippets})

@login_required
def comment_delete(request, comment_id):
    '''
    User wants to delete an existing snippet
    '''
    comment_d = get_object_or_404(Comment, id=comment_id)

    if request.user != comment_d.user:
        raise Http404
    # perform_delete(request, comment_d)
    comment_d.delete()
    return http.HttpResponseRedirect(comment_d.snippet.get_absolute_url())




@login_required
def snippet_delete(request, snippet_id):
    '''
    User wants to delete an existing snippet
    '''
    snip_d = get_object_or_404(Snippet, id=snippet_id)

    if request.user == snip_d.user:
        snip_d.delete()
        return render(request, 'csnip/snippet/delete.html')
    else:
        raise PermissionDenied

@login_required
def snippet_edit(request,pk):
    '''
    User wants to edit their own snippet.
    '''
    snip_e = get_object_or_404(Snippet, pk=pk)
    if request.user == snip_e.user:
        if request.method == 'POST':
            form  = SnippetEditForm(request.POST, instance=snip_e)
            if form.is_valid():
                snip_e = form.save(commit=False)
                snip_e.user = request.user
                snip_e.updated = timezone.now()
                s_tags = form.cleaned_data['tags']
                snip_e.tags.add(*s_tags)

                snip_e.save()
                messages.success(request, "Snippet Updated Successfully")
                return redirect(snip_e.get_absolute_url())
        else:
            form = SnippetEditForm(instance=snip_e)

    return render(request, 'csnip/snippet/edit.html',{'section':'snippet', 'form':form})


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
            # s = new_item.title[::-1]+new_item.explanation[:5]+uuid.uuid4().hex[:6].upper()
            s = new_item.title+'-'+uuid.uuid4().hex[:6].upper()
            new_item.slug = slugify(s)
            # assign current user to the snippet
            new_item.user = request.user
            # s_tags = form.cleaned_data['tags']
            # new_item.tags.add(*s_tags )
            new_item.save()
            create_action(request.user, 'created snippet', new_item)
            form.save_m2m()


            messages.success(request, "Snippet Added Successfully")

            # redirect to newly created item detail view
            # try:
            return redirect(new_item.get_absolute_url())
            # except:



    else:
        form = SnippetCreateForm()

    return render(request, 'csnip/snippet/create.html',{'section':'snippet', 'form':form})




@login_required
@require_POST
def snip_like(request):

    snip_id = request.POST.get('id')
    action = request.POST.get('action')
    if snip_id and action:
        try:
            snippet = Snippet.publishedd.get(id=snip_id)
            # create_action(request.user, 'likes', image)
            if action == 'like':
                snippet.user_like.add(request.user)
                create_action(request.user, 'likes', snippet)
            else:
                snippet.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
