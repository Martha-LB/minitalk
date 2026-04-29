from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Post, Comment, Profile, Follow
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .forms import UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def post(request):
    query = request.GET.get("q", "").strip()

    posts = Post.objects.filter(user = request.user)
    if query:
        posts = posts.filter(
            Q(content__icontains=query)
        )
    posts = posts.order_by("-created_at")
    count = posts.count()
    paginator = Paginator(posts, 20)   # 每页20条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "post.html", {
        'page_obj': page_obj, 
        "mode": "mine", 
        "query": query,
        "count": count,
        })

@login_required
def public_post(request):
    query = request.GET.get("q", "").strip()

    posts = Post.objects.filter(is_public=True)

    if query:
        posts = posts.filter(
            Q(content__icontains=query)
        )
    posts = posts.order_by("-created_at")
    paginator = Paginator(posts, 20)   # 每页20条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "post.html", {'page_obj': page_obj, "mode": "public", "query": query,})


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        is_public = request.POST.get("is_public") == "on"
        if content:
            Post.objects.create(user=request.user, content=content.strip(),is_public=is_public)
    posts = Post.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, "create_post.html", {"posts":posts})

def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if post.user == request.user:
            post.delete()
    return redirect(request.META.get("HTTP_REFERER", "post"))

@login_required
def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content")
        if content and content.strip():
            Comment.objects.create(post=post,user=request.user, content=content.strip())

    referer = request.META.get("HTTP_REFERER", "/post/")
    parsed = urlparse(referer)
    query_params = parse_qs(parsed.query)

    query_params["open_comment"] = [str(post_id)]

    new_query = urlencode(query_params, doseq=True)
    new_fragment = f"post-{post_id}"

    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        new_fragment,
    ))

    return redirect(new_url)


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


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 只允许作者编辑
    if post.user != request.user:
        return redirect("post")

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            post.content = content
            post.is_public = request.POST.get("is_public") == "on"
            post.save()

        post.is_public = request.POST.get("is_public") == "on"
        return redirect("post")

    return render(request, "edit_post.html", {"post": post})


@login_required
def profile_view(request):
    profile = request.user.profile
    following = Follow.objects.filter(follower=request.user)
    followers = Follow.objects.filter(following=request.user)


    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        bio = request.POST.get("bio", "").strip()

        if username:
            from django.contrib.auth.models import User
            if User.objects.exclude(id=request.user.id).filter(username=username).exists():
                error = "This username is already taken."
            else:
                request.user.username = username
                request.user.save()

                profile.bio = bio
                if "avatar" in request.FILES:
                    profile.avatar = request.FILES["avatar"]
                profile.save()

                return redirect("profile")
        else:
            error = "Username cannot be empty."

    return render(request, "profile.html", {
        "profile": profile,
        "error": error,
        "following": following,
        "followers": followers,
    })

def user_profile_view(request, user_id):

    user_obj = get_object_or_404(User, id=user_id)
    profile = user_obj.profile
    posts = Post.objects.filter(user=user_obj, is_public=True).order_by("-created_at")

    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    return render(request, "user_profile.html", {
        "profile_user": user_obj,
        "profile": profile,
        "posts": posts,
        "is_following": is_following,
    })



@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        if target_user != request.user:
            Follow.objects.get_or_create(
                follower=request.user,
                following=target_user
            )
    return redirect("user_profile", user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).delete()
    return redirect("user_profile", user_id=user_id)