from django.shortcuts import render, get_object_or_404
from .models import Post



#Renders all blog posts

def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post':post
    }
    return  render(request, 'blog/post_detail.html', context)










