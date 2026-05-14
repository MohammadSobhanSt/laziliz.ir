from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordResetView


app_name = 'accounts'
urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/explore/<str:username>/', views.UserProfileExploreView.as_view(), name='profile-explore'),
    path('follow/<str:username>/', views.UserFollowView.as_view(), name='user-follow'),
    path('unfollow/<str:username>/', views.UserUnfollowView.as_view(), name='user-unfollow'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/user/<int:user_id>', views.UserDeleteView.as_view(), name='delete'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
]