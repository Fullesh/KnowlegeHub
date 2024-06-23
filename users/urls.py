from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, OTPConfirmView, UserDetailView, MyLoginView, UserDeleteView, res_password

app_name = UsersConfig.name
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', OTPConfirmView.as_view(), name='otp_confirm'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
    path('reset_password/', res_password, name='reset_password')
]
