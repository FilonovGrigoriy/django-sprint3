from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BasePublishedModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        help_text='Дата и время добавления.',
    )

    class Meta:
        abstract = True


class Category(BasePublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )
    description = models.TextField(
        'Описание',
        help_text='Опишите, для каких публикаций эта категория.',
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(BasePublishedModel):
    name = models.CharField(
        'Название места',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(BasePublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )
    text = models.TextField(
        'Текст',
        help_text='Основной текст публикации.',
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
        help_text='Автор, создавший эту публикацию.',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
        help_text=(
            'Место, к которому относится публикация '
            '(можно не указывать).'
        ),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
        help_text='Категория, к которой относится публикация.',
    )

    @classmethod
    def public_posts(cls):
        return (
            cls.objects
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
            .select_related('author', 'category', 'location')
        )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
