from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post
from .models import Category


def index(request):
    template = "blog/index.html"
    now = timezone.now()
    posts = (
        Post.objects.all()
        .filter(
            pub_date__lte=now,
            is_published=True,
            category__is_published=True)
        .order_by("-pub_date")[0:5]
    )
    content = {"post_list": posts}
    return render(request, template, content)


def category_posts(request, category_slug):
    template = "blog/category.html"
    now = timezone.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
    )
    if not category.is_published:
        raise Http404(f"Category {category_slug} is invalid.")
    posts = (
        Post.objects.all()
        .filter(
            pub_date__lte=now,
            category=category,
            is_published=True,
            category__is_published=True,
        )
        .order_by("-pub_date")
    )
    content = {"category": category, "post_list": posts}
    return render(request, template, content)


def post_detail(request, pk):
    template = "blog/detail.html"
    now = timezone.now()
    post = get_object_or_404(Post, pk=pk)
    if (post.pub_date > now
            or not post.is_published
            or not post.category.is_published):
        raise Http404("This post is invalid.")
    content = {"post": post}
    return render(request, template, content)
