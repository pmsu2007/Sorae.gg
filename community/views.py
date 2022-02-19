from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from community.models import Post, Comment
from community.forms import PostForm

def index(request):
    post_list = Post.objects.order_by('-create_date')
    context = {'post_list': post_list}
    return render(request, 'community/post_list.html', context)


def detail(request, post_id):
    """
    detail 내용 출력
    """
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'community/post_detail.html', context)


def comment_create(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    comment = Comment(post=post, content=request.POST.get('content'), create_date=timezone.now())
    comment.save()
    return redirect('community:detail', post_id=post.id)


def post_create(request):
    post = Post(subject=request.POST.get('subject'), content=request.POST.get('content'), create_date=timezone.now())
    post.save()
    return redirect('community:index')


def editor(request):
    form = PostForm()
    return render(request, 'community/post_editor.html', {'form': form})
