from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from community.models import Post, Comment
from community.forms import PostForm, CommentForm
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

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = post
            answer.post_id = post.id
            answer.save()
            return redirect('community:detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'community/post_detail.html', context)


def post_editor(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('community:list')
    else:
        form = PostForm()
        context = {'form': form}
        return render(request, 'community/post_editor.html', context)

