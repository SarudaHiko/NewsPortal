from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .utilits import DAY_POST_LIMIT


class PostsList(ListView, PermissionRequiredMixin):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    permission_required = ('news.view_post',)

    def get_queryset(self):
        if ('AT' in self.request.path) or ('NW' in self.request.path):
            context = Post.objects.filter(p_type=self.kwargs['p_type'])
        else:
            context = Post.objects.all()
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        if (Post.TP[0][0] in self.request.path) or (Post.TP[1][0] in self.request.path):
            context['quantity'] = Post.objects.filter(p_type=self.kwargs['p_type']).count()

        if Post.TP[0][0] in self.request.path:
            context['title'] = 'Статьи'
        elif Post.TP[1][0] in self.request.path:
            context['title'] = 'Новости'
        else:
            context['title'] = 'Все публикации'
            context['no_type'] = True
            context['quantity'] = Post.objects.all().count()
        return context


class PostDetail(DetailView, PermissionRequiredMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    permission_required = ('news.view_post',)


class PostSearch(ListView):
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Поиск публикации'}
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['quantity'] = self.filterset.qs.all().count()
        if 'do_search' in self.request.GET:
            context['is_search'] = True
        return context


class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if Post.TP[0][0] in self.request.path:
            context['title'] = 'Добавить статью'
        elif Post.TP[1][0] in self.request.path:
            context['title'] = 'Добавить новость'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        if Post.TP[0][0] in self.request.path:
            post.p_type = Post.TP[0][0]
        elif Post.TP[1][0] in self.request.path:
            post.p_type = Post.TP[1][0]
        return super().form_valid(form)


class PostEdit(UpdateView, PermissionRequiredMixin):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Редактировать публикацию'}


class PostDelete(DeleteView, PermissionRequiredMixin):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    extra_context = {'title': 'Удалить публикацию'}


@login_required
def subscribe_me(request, slug):
    user = request.user
    category = Category.objects.get(slug=slug)
    categories = Category.objects.filter(subscribers__username=user)
    if category not in categories:
        category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


def post_limit_spent_view(request):
    title = 'Имя_подписчика',
    limit = DAY_POST_LIMIT
    return render(request, 'post_limit_spent.html', {'title': title, 'limit': limit})


def mail_notify_new_post_view(request):
    msg_data = {'subscriber_name': 'Имя_подписчика',
        'new_post_title': 'Заголовок_новой_публикации',
        'author_first_name': 'Имя_автора',
        'author_last_name': 'Фамилия_автора',
        'new_post_time': 'Время_выхода_новой_публикации',
        'new_post_text': 'Текст_новой_публикации',
        'new_post_pk': '7',
    }
    return render(request, 'notify_new_post.html', {'msg_data': msg_data, })


def mail_weekly_notify_posts_view(request):
    posts = Post.objects.filter(category__slug='it').values('id', 'title', 'time')
    msg_data = {'subscriber_name': 'Имя_подписчика', 'posts': posts}
    return render(request, 'weekly_notify_posts.html', {'msg_data': msg_data, })
