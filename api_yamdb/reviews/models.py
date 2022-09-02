from django.db import models

from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
        help_text='Категория, к которой будет относиться произведение'
    )
    slug = models.SlugField(
        max_length=15,
        unique=True,
        db_index=True,
        verbose_name='URL-идентификатор категории',
        help_text=(
            'Уникальная строка, содержащая только "безопасные" символы'
        )
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
        help_text='Жанр, к которому будет относиться произведение'
    )
    slug = models.SlugField(
        max_length=15,
        unique=True,
        verbose_name='URL-идентификатор жанра',
        help_text=(
            'Уникальная строка, содержащая только "безопасные" символы'
        )
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название произведения',
        help_text='Название нового произведения'
    )
    year = models.PositiveIntegerField(
        verbose_name='Дата создания произведения',
        help_text='Дата создания произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        blank=True,
        verbose_name='Жанр произведения',
        help_text='Жанр, к которому будет относиться произведение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Категория, к которой относится произведение'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание произведения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, на которое написан отзыв'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Напишите отзыв на произведение',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviewer',
        verbose_name='Пользователь',
        help_text='Пользователь, желающий написать отзыв'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(10), MinValueValidator(1)),
        verbose_name='Оценка произведения',
        help_text='Оценка произведения от 1 до 10',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата создания отзыва')

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_pair'
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, на которое написан комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите комментарий на отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
        help_text='Пользователь, желающий написать комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата создания комменатрия')

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
