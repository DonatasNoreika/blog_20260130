from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Post, Comment
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def posts(request):
    posts = Post.objects.order_by("-pk")
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)
    context = {
        'posts': paged_posts,
    }
    return render(request, template_name="posts.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


def search(request):
    query = request.GET.get('query')

    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__username__icontains=query) |
        Q(author__first_name__icontains=query) |
        Q(author__last_name__icontains=query))


    context = {
        "query": query,
        "posts": posts,
    }
    return render(request, template_name="search.html", context=context)


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "userposts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "usercomments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)
