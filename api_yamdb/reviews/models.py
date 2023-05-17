import datetime

from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator)
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

from reviews.services import validate_name_me

ROLE_SET = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class UserManager(BaseUserManager):
    """Новые правила регистрации юзера."""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email обязателен.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')  # установка роли 'admin'
        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперюзера поле должно быть is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперюзера должно быть is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class YaMdbUser(AbstractUser):
    """Переопределенная модель пользователя."""
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_LENGTH_USERNAME,
        unique=True,
        validators=[validate_name_me]
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Уровень доступа',
        max_length=15,
        choices=ROLE_SET,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтвержедния',
        max_length=settings.MAX_LENGTH_CODE,
        null=True,
        blank=False,
        default=None
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    object = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                    message='Некорректный slug.')]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                    message='Некорректный slug.')]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(null=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    rating = models.IntegerField(blank=True, null=True,)

    class Meta:
        ordering = ('name', 'year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи многим ко многим произведения и жанра."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Жанр-произведение'
        verbose_name_plural = 'Жанры-произведения'


class Review(models.Model):
    """Модель для отзывов к произведениям."""
    author = models.ForeignKey(
        YaMdbUser, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text[:settings.TEXT_LIMIT]


class Comment(models.Model):
    """Модель для комментариев к отзывам."""
    author = models.ForeignKey(
        YaMdbUser, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.TEXT_LIMIT]
