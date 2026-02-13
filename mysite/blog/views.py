from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import UserChangeForm, ProfileChangeForm, PostCommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

def posts(request):
    posts = Post.objects.order_by("-pk")
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)
    context = {
        'posts': paged_posts,
    }
    return render(request, template_name="posts.html", context=context)


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form_class = PostCommentForm

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


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


@login_required
def profile(request):
    u_form = UserChangeForm(request.POST or None, instance=request.user)
    p_form = ProfileChangeForm(request.POST or None, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        return redirect("profile")

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, template_name="profile.html", context=context)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "form.html"
    fields = ['title', 'content', 'cover']
    success_url = reverse_lazy('userposts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "form.html"
    fields = ['title', 'content', 'cover']

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user

