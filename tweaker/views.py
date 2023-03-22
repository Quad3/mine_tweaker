from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Post
from .forms import PostForm


class HomePageView(ListView):
    template_name = 'tweaker/posts.html'
    queryset = Post.objects.all()
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
