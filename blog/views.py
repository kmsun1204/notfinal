from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CreatePostForm, PostSearchForm
from django.views.generic.edit import FormView
from django.db.models import Q
import datetime


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10


class PostDetailView(generic.DetailView):
    model = Post


def get_nick(user):
    conn_user = user
    conn_profile = User.objects.get(email=conn_user)
    nick = conn_profile.username
    return nick


@login_required
def post_write(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            conn_user = request.user
            conn_profile = get_object_or_404(User, email=conn_user)
            nick = conn_profile.username
            new_post = form.save(commit=False)
            new_post.writer = nick
            new_post.save()
            messages.info(request, '글을 성공적으로 올렸습니다!')
            return HttpResponseRedirect(reverse_lazy('board_index'))
    else:
        form = CreatePostForm()

    return render(request, 'blog/write_post.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk = pk)
    context = {'post': post}
    # 저장 과정
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        conn_user = request.user
        nick = get_nick(conn_user)

        if nick != post.writer:
            messages.info(request, '권한이 없습니다!')
            return render(request, 'blog/post_detail.html', context=context)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_date = datetime.datetime.now()
            post.save()
            messages.info(request, '성공적으로 수정되었습니다!')
            return render(request, 'blog/post_detail.html', context=context)
    # 전송 폼
    else:
        title = post.post_title
        content = post.post_contents
        form = CreatePostForm(initial={'post_title': title, 'post_contents': content,})

    return render(request, 'blog/write_post.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('board_index')


@login_required
def comment_write(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        context = {'post': post}
        content = request.POST.get('content')

        conn_user = request.user
        conn_profile = User.objects.get(email=conn_user)

        if not content:
            messages.info(request, 'You dont write anything....')
            return render(request, 'blog/post_detail.html', context=context)

        Comment.objects.create(post=post, comment_writer=conn_profile, comment_contents=content)
        return render(request, 'blog/post_detail.html', context=context)


@login_required
def comment_delete(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)

    context = {'post' : post,}
    content = request.POST.get('content')

    conn_user = request.user
    conn_profile = User.objects.get(email=conn_user)

    if conn_profile != comment.comment_writer:
        messages.info(request, '권한이 없습니다!')
        return render(request, 'blog/post_detail.html', context=context)

    comment.delete()
    return render(request, 'blog/post_detail.html', context=context)


class SearchFormView(FormView):
    # form_class를 forms.py에서 정의했던 PostSearchForm으로 정의
    form_class = PostSearchForm
    template_name = 'search/search.html'

    # 제출된 값이 유효성검사를 통과하면 form_valid 메소드 실행
    # 여기선 제출된 search_word가 PostSearchForm에서 정의한대로 Char인지 검사
    def form_valid(self, form):
        # 제출된 값은 POST로 전달됨
        # 사용자가 입력한 검색 단어를 변수에 저장
        search_word = self.request.POST['search_word']
        # Post의 객체중 제목이나 설명이나 내용에 해당 단어가 대소문자관계없이(icontains) 속해있는 객체를 필터링
        # Q객체는 |(or)과 &(and) 두개의 operator와 사용가능
        post_list = Post.objects.filter(Q(post_title__icontains=search_word) | Q(writer__icontains=search_word) |
                                        Q(post_contents__icontains=search_word))

        context = {}
        # context에 form객체, 즉 PostSearchForm객체 저장
        context['form'] = form
        context['search_term'] = search_word
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)
