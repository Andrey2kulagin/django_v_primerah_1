from django.shortcuts import render, get_object_or_404
from .models import Post, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentsForm
from taggit.models import Tag


# Create your views here.

def post_list(request, tag_slug=None):
    context = {}
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context['posts'] = posts
    context['page'] = page
    context['tag'] = tag
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    context = {}

    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.post = post
            object.save()
    comments = reversed(post.comments.all())
    form = CommentsForm()
    context['post'] = post
    context['form'] = form
    context["comments"] = comments
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    context = {}
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    context['form'] = form
    return render(request, 'blog/post/share.html', context)
