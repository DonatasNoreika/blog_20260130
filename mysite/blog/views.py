from django.shortcuts import render
from .models import Post

def posts(request):
    context = {
        'posts': Post.objects.order_by("-pk"),
    }
    return render(request, template_name="posts.html", context=context)