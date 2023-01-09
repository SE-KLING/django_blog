from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from enumfields import EnumField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from blog.enums import PostStatus


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField()
    modified_at = AutoLastModifiedField()

    class Meta:
        abstract = True


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=PostStatus.PUBLISHED)


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published_at')
    body = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    status = EnumField(PostStatus, default=PostStatus.DRAFT)
    # Managers
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published_at.year, self.published_at.month,
                                                 self.published_at.day, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]
