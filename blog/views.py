from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import PostForm, CommentForm


#Renders all blog posts using a class (new)
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

#Shows specific users ass post.
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)


#Renders all blog posts using a function (old)
'''
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
'''


#Show's a specific blog post and renders that posts details using a class (new)

class PostDetailView(DetailView):
    model = Post

#Show's a specific blog post and renders that posts details using a function (old)
'''
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)
'''

# Create a new post using a class view (new)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'text']


    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)



# Create a new post using a function (old)
'''
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
'''


# Update an existing post using class method
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Update an existing
'''
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
'''

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


#class that deletes a post (new)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


#Function that deletes a post (old)
'''
@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
'''


# class that creates a comment on a specific post. (new)
class AddCommentToPostView(CreateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.post = post
        if self.request.user.username != '':
            form.instance.approved = True
        return super().form_valid(form)

# Function that creates a comment on a specific post. (old)
'''
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            print(comment.post)

            if request.user.username == '':
                comment.save()
            else:
                comment.approved = True
                comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
'''

# class that removes specific comments (new)
class CommentRemoveView(UserPassesTestMixin,DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})
        else:
            return reverse_lazy('post_detail', args=(self.object.post.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.post = post
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.username == post.author or self.request.user.is_superuser :
            return True
        return False


'''
# Function that removes specific comments (old)
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
'''

# Function to aprove AnnonymousUsers comments
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


