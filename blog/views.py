from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


#Renders all blog posts

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)

#Show's a specific blog post and renders that posts details

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


# Create a new post

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        context = {'form': form}
        return render(request, 'blog/post_edit.html', context)


# Update an existing post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {'form': form, 'post':post}
        return render(request, 'blog/post_edit.html', context)


#Shows all the posts that are created, but aren't published yet
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True)
    context = {'posts': posts}

    return render(request, 'blog/post_draft_list.html', context)


#Publishes a post
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


