from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from hyostagram.custom_login_required import custom_login_required

from .models import Post, Comment
from .forms import CommentForm, PostForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }

    return render(request, 'post/post_detail.html', context)

@login_required
def comment_create(request, post_pk):
    # GET으로 전달된 값으로 완료 후 이동할 URL
    next_path = request.GET.get('next')


    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)

        user = get_user_model()
        row = user.objects.get(pk=1)

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = row

            comment.save()

            messages.success(request, '댓글이 등록되었습니다.')
        else:
            error_msg = '댓글 등록에 실패했습니다\n{}'.format(
                '\n'.join(
                    [f'-{error}'
                     for key, value in comment_form.errors.items()
                     for error in value]))
            messages.error(request, error_msg)
        #next파라미터가 있을 경우 지정된 이동 경로로 이동
        if next_path:
            return redirect(next_path)
        return redirect('post:post_list')

@login_required
def post_create(request):
    if request.method == 'POST':
        #Postform은 파일도 처리하므로 request.FILES 추가
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = get_user(request)
            post.save()

            messages.success(request, '사진이 등록되었습니다.')
            return redirect('post:post_list')

    else:
        post_form = PostForm()

    ctx = {
        'post_form': post_form,
    }
    return render(request, 'post/post_create.html', ctx)

