from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html',
                  context={'page_obj': page_obj})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/group_list.html',
                  context={'group': group,
                           'posts': posts,
                           'page_obj': page_obj})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    posts_count = Post.objects.filter(author=user).count  
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/profile.html',
                  context={'author': user,
                           'page_obj': page_obj,
                           'posts_count': posts_count})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None,)
    if request.method == "GET" or not form.is_valid():
        return render(request, "posts/create_post.html",
                      context={"form": form})
    else:
        form.instance.author = request.user
        form.save()
        return redirect("posts:profile", request.user.username)  


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.filter(pk=post_id))
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if post.author.pk != request.user.id:
        return redirect("posts:post_detail", post_id)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)

    return render(request, "posts/create_post.html",
                  context={'form': form,
                           'is_edit': True,
                           'post': post})