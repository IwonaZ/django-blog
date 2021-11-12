from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Blog
from  django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def home(request):
    context = {
        'posts': Blog.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Blog
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']

class PostDetailView(DetailView):
    model = Blog

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
