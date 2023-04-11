from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Comment
from .forms import PostForm, CommentForm


class HomePageView(ListView):
    template_name = 'tweaker/posts.html'
    queryset = Post.objects.select_related('owner')
    context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tweaker/post-create.html'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        print(self.object)
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tweaker/post-detail.html'
    queryset = Post.objects.select_related('owner')
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related('owner')\
            .filter(post=context['post'])
        return context


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, post_pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.owner = request.user
            new_comment.save()

        return redirect('post_detail', post_pk)
