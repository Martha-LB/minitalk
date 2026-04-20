from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "base.html")

@login_required
def post(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post.html", {"posts":posts})

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Post.objects.create(user=request.user, content=content.strip())
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "create_post.html", {"posts":posts})

def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if post.user == request.user:
            post.delete()
    return redirect(request.META.get("HTTP_REFERER", "post"))

def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content")
        if content and content.strip():
            Comment.objects.create(post=post,user=request.user, content=content.strip())
    return redirect("post")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "register.html", {
                "error": "The two passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "This username is already taken."
            })

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect("post")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {
                "error": "Invalid username or password."
            })

        login(request, user)
        return redirect("post")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 只允许评论作者删除
    if comment.user == request.user or comment.post.user == request.user:
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'post'))
