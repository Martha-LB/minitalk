from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post/", views.post, name="post"),
    path("create_post/", views.create_post, name="create_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("comment/<int:post_id>/", views.create_comment, name="create_comment"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("feed/", views.public_post, name="public_post"),
]