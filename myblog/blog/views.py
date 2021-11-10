from django.shortcuts import render
from .models import Blog

# Create your views here.

def home(request):
    context = {
        'posts': Blog.objects.all()
    }
    return render(request, 'blog/home.html', context)

# def blog_post(request, id=1):
#     blog = Blog.objects.get(id=id)
#     context = {'blog': blog}
#     return render(request, 'blog/blog_post.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': "About page"})

