from django.http import Http404
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timezone

from .models import Post
from .models import Category


def index(request):
    template = "blog/index.html"
    posts = (
        Post.objects.all()
        .filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )
        .order_by("-pub_date")[0:5]
    )
    content = {"post_list": posts}
    return render(request, template, content)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category,
        slug=category_slug,
    )
    if not category.is_published:
        raise Http404(f"Category {category_slug} is invalid.")
    posts = Post.objects.all().filter(
            category=category,
            is_published=True,
            category__is_published=True,).order_by("-pub_date")
    content = {"category": category, "post_list": posts}
    return render(request, template, content)


def post_detail(request, pk):
    template = "blog/detail.html"
    post = get_object_or_404(Post, pk=pk)
    if (
        post.pub_date > datetime.now()
        and post.is_published
        and post.category.is_published
    ):
        raise Http404(f"This post is invalid.")
    content = {"post": post}
    return render(request, template, content)
