from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import PostForm
from datetime import datetime
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Response
from .forms import ResponseForm
from django.conf import settings
from .signals import send_notification_resp
from django.contrib.sites.models import Site
from django.shortcuts import redirect


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = 'text'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('responses')  # Загружаем связанные отклики заранее
        return queryset


class PostCreate(CreateView):
    permission_required = ('new.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)



class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        post = self.get_object()
        responses = post.responses.filter(accepted=True)  # Получить только принятые отклики
        context['responses'] = responses
        context['form'] = ResponseForm()
        return context



    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
        return redirect('post_detail', pk=post.pk)

        # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     return context

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('new.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('new.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


def post_responses(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if request.method == 'POST':
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        if action == 'accept':
            response = get_object_or_404(Response, pk=response_id)
            response.accepted = True
            response.save()
        elif action == 'reject':
            response = get_object_or_404(Response, pk=response_id)
            response.accepted = False
            response.save()

    responses = Response.objects.filter(post=post)
    return render(request, 'post_responses.html', {'post': post, 'responses': responses})


@login_required
def author_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user)

    if request.method == 'POST':
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        if action == 'accept':
            response = get_object_or_404(Response, pk=response_id)
            response.accepted = True
            response.save()
        elif action == 'reject':
            response = get_object_or_404(Response, pk=response_id)
            response.delete()

    return render(request, 'author_posts.html', {'posts': posts})
# def author_posts(request):
#     user = request.user
#     posts = Post.objects.filter(author=user)
#     has_posts = posts.exists()  # Проверяем наличие статей
#
#     if request.method == 'POST':
#         response_id = request.POST.get('response_id')
#         action = request.POST.get('action')
#
#         if action == 'accept':
#             response = get_object_or_404(Response, pk=response_id)
#             response.accepted = True
#             response.save()
#         elif action == 'reject':
#             response = get_object_or_404(Response, pk=response_id)
#             response.accepted = False
#             response.save()
#
#     return render(request, 'author_posts.html', {'posts': posts, 'has_posts': has_posts})

class AuthorPostsView(ListView):
    model = Post
    template_name = 'author_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.request.user  # Получаем текущего авторизованного пользователя как автора постов
        context['responses'] = Response.objects.filter(post__author=author)  # Получаем все отклики автора
        return context

    def post(self, request, *args, **kwargs):
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        if response_id and action:
            response = get_object_or_404(Response, id=response_id)

            if action == 'accept':  # Принять отклик
                response.accepted = True
                response.save()
                # Отправить уведомление об принятии отклика на почту пользователю
                send_notification_resp(sender=Response, instance=response, created=True)

            elif action == 'reject':  # Отклонить отклик
                # Сначала отправляем уведомление на почту пользователю
                send_notification_resp(sender=Response, instance=response, created=True)
                # Затем удаляем отклик
                response.delete()

        return redirect('author_posts')




