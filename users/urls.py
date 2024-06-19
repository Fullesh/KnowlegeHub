from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.models import User
from users.views import HomePageView, RegisterView, OTPConfirmView, UserDetailView

app_name = UsersConfig.name
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/user_login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', OTPConfirmView.as_view(), name='otp_confirm'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='detail')
]
