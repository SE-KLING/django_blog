# Generated by Django 4.1.5 on 2023-01-06 10:59

import blog.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_at', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250)),
                ('body', models.TextField()),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', enumfields.fields.EnumField(default='DF', enum=blog.enums.PostStatus, max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-published_at'], name='blog_post_publish_2c9212_idx'),
        ),
    ]