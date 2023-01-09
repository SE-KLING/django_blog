from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.enums import PostStatus
from blog.forms import EmailPostForm
from blog.models import Post


def post_detail(request, year, month, day, post):
    filter_criteria = {
        'status': PostStatus.PUBLISHED,
        'slug': post,
        'published_at__year': year,
        'published_at__month': month,
        'published_at__day': day,
    }
    post = get_object_or_404(Post, **filter_criteria)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_list(request):
    posts_qs = Post.published.all()
    paginator = Paginator(posts_qs, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_share(request, post_id):
    blog_post = get_object_or_404(Post, id=post_id, status=PostStatus.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            blog_post_url = request.build_absolute_uri(blog_post.get_absolute_url())
            sender, receiver, comments = cd['name'], cd['to'], cd['comments']
            subject = f'{cd["name"]} recommends you read {blog_post.title}'
            message = f'Read {blog_post.title} at {blog_post_url} \n {sender}\"s comments: {comments}'
            send_mail(subject, message, 'stefankling18@gmail.com', [receiver, ])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': blog_post, 'form': form, 'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
