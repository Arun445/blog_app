from django.shortcuts import render
from .models import Post

# Create your views here.

def post_list(request):
    blog_title = Post.objects.all().order_by('-published_date')
    context = {
        'i': blog_title
    }
    return render(request, 'blog/post_list.html', context)