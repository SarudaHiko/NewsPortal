from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author


class PostsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        if ('AT' in self.request.path) or ('NW' in self.request.path):
            context = Post.objects.filter(p_type=self.kwargs['p_type'])
        else:
            context = Post.objects.all()
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

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


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

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
        # current_user = self.request.user
        # post.author = Author.objects.get(author_acc=current_user)
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Редактировать публикацию'}


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    extra_context = {'title': 'Удалить публикацию'}
