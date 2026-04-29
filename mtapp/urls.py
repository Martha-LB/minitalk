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
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("profile/", views.profile_view, name="profile"),
    path("user/<int:user_id>/", views.user_profile_view, name="user_profile"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("api/comment/<int:post_id>/", views.create_comment_api, name="create_comment_api"),
    path("api/comment/<int:comment_id>/delete/", views.delete_comment_api, name="delete_comment_api"),
    path("api/post/<int:post_id>/delete/", views.delete_post_api, name="delete_post_api"),
    path("api/translate/", views.translate_api, name="translate_api"),
]