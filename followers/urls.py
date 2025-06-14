from django.urls import path
from . import views

urlpatterns = [
    path('followers/',views.ListFollowers.as_view()),
    path('followings/',views.ListFollowing.as_view()),
    path('follow/<int:followed_user_id>',views.FollowUser.as_view()),
    path('unfollow/<int:followed_user_id>/',views.UnfollowUser.as_view())
]
