from django.shortcuts import render, get_object_or_404

from .models import Category, Post

POSTS_LIMIT = 5


def index(request):
    """Главная страница: 5 последних опубликованных постов."""
    posts = Post.public_posts().order_by('-pub_date')[:POSTS_LIMIT]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Страница одного поста.

    404, если:
    - пост не опубликован;
    - дата публикации в будущем;
    - категория поста снята с публикации.
    Локация не влияет на показ.
    """
    post = get_object_or_404(
        Post.public_posts(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории.

    404, если категория снята с публикации.
    Показываются только опубликованные посты этой категории
    с датой публикации не позже текущего момента.
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = (
        Post.public_posts()
        .filter(category=category)
        .order_by('-pub_date')
    )
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
