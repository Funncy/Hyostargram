from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib import messages

from .models import Post, Comment
from .forms import CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
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


def comment_create(request, post_pk):
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

        return redirect('post_list')


