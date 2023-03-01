from django.shortcuts import render, get_object_or_404
from .models import Post, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentsForm


# Create your views here.

def post_list(request):
    context = {}
    object_list = Post.published.all()
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
    return render(request, 'blog/post/list.html', context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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
    comments = reversed(Comments.objects.filter(post=post))
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
