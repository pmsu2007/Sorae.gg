from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views import generic
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tools.tool import *
from community.models import *
from community.forms import *

'''
 나중에, View name 리팩토링 해야 됨 
'''


def post_list(request, category):
    page = request.GET.get('page', '1')
    keyword = request.GET.get('keyword', '')
    target = request.GET.get('target', '')
    sort = request.GET.get('sort', '')

    # 카테고리
    post_list = Post.objects.all()

    if category != "all":
        post_list = Post.objects.filter(category_name=category)

    # 정렬
    if sort == "popular":
        post_list = post_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    else:
        post_list = post_list.order_by('-create_date')

    # 검색
    if keyword:
        if target == "subject":
            post_list = post_list.filter(Q(subject__icontains=keyword)).distinct()
        elif target == "content":
            post_list = post_list.filter(Q(content__icontains=keyword)).distinct()
        elif target == "user_name":
            post_list = post_list.filter(Q(author__username__icontains=keyword)).distinct()

    # 페이징 처리
    paginator = Paginator(post_list, 15)  # 페이지당 15개의 Post 출력
    pageObj = paginator.get_page(page)

    context = {'post_list': pageObj, 'page': page, 'keyword': keyword, 'sort': sort, 'category': category}
    return render(request, 'community/post_list.html', context)


def post_detail(request, post_id):
    """
    detail 내용 출력
    """
    post = get_object_or_404(Post, pk=post_id)

    # 조회수
    ip = get_client_ip(request)
    register = PostHits.objects.filter(ip=ip, post=post).count()
    if register == 0:
        h = PostHits(ip=ip, post=post)
        h.save()
        post.hits += 1
        post.save()

    context = {'post': post}
    return render(request, 'community/post_detail.html', context)


@login_required(login_url='common:login')
def post_editor(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('community:list', category=post.category_name)
    else:
        form = PostForm()
        context = {'form': form}
        return render(request, 'community/post_editor.html', context)


@login_required(login_url='common:login')
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('community:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'community/post_editor.html', context)


@login_required(login_url='common:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('community:list', category=post.category_name)


@login_required(login_url='common:login')
def post_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.voter.add(request.user)
    return redirect('community:detail', post_id=post.id)


@login_required(login_url='common:login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.question = post
            comment.post_id = post.id
            comment.author = request.user
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('community:detail', post_id=post.id), comment.id))
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'community/post_detail.html', context)


@login_required(login_url='common:login')
def comment_delete(request, post_id ,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('community:detail', post_id=post_id)


@login_required(login_url='common:login')
def comment_vote(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.voter.add(request.user)
    return redirect('{}#comment_{}'.format(resolve_url('community:detail', post_id=post_id), comment.id))