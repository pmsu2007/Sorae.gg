from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from community.models import Post, Comment
from django.core.paginator import Paginator



def list(request):

    page = request.GET.get('page', '1')

    # 조회
    postList = Post.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(postList, 15) # 페이지당 10개의 Post 출력
    pageObj = paginator.get_page(page)

    context = {'post_list': pageObj}
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
    return render(request, 'community/post_editor.html')
