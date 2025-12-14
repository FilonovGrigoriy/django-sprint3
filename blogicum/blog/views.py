from django.shortcuts import get_object_or_404, render

from .models import Category, Post

POSTS_LIMIT = 5


def index(request):
    posts = (
        Post.public_posts()
        .select_related('author', 'category', 'location')
        .order_by('-pub_date')[:POSTS_LIMIT]
    )
    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
            'title': 'Лента записей',
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.public_posts().select_related('author', 'category', 'location'),
        pk=post_id,
    )
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'title': post.title,
        },
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = (
        Post.public_posts()
        .filter(category=category)
        .select_related('author', 'category', 'location')
        .order_by('-pub_date')
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'posts': posts,
            'title': category.title,
        },
    )
