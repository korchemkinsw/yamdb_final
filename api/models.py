from django.db import models
from django.db.models.functions import Length
from slugify import slugify
from users.models import User

from .validators import not_future_year_validator, validate_score

models.CharField.register_lookup(Length)
models.TextField.register_lookup(Length)


class Category(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='название категории',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='category_name_not_empty'
            ),
            models.CheckConstraint(
                check=models.Q(slug__length__gt=0),
                name='category_slug_not_empty'
            )
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='название жанра',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='genre_name_not_empty'
            ),
            models.CheckConstraint(
                check=models.Q(slug__length__gt=0),
                name='genre_slug_not_empty'
            )
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='название',
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    year = models.IntegerField(
        verbose_name='год создания',
        validators=[not_future_year_validator]
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='title_name_not_empty'
            )
        ]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='отзыв',
        related_name='reviews'
    )
    text = models.TextField(max_length=300)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор отзыва',
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[validate_score]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__lt=11),
                name='score_less_than_11'
            ),
            models.CheckConstraint(
                check=models.Q(score__gt=0),
                name='score_is_possitive'
            ),
            models.CheckConstraint(
                check=models.Q(text__length__gt=0),
                name='review_text_not_empty'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField(max_length=300)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-pub_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(text__length__gt=0),
                name='comment_text_not_empty'
            )
        ]
