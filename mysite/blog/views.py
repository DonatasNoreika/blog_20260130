from django.shortcuts import render
from .models import Post
from django.views import generic

def posts(request):
    context = {
        'posts': Post.objects.order_by("-pk"),
    }
    return render(request, template_name="posts.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

