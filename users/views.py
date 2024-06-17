import random

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from config import settings
from users.forms import UserRegisterForm
from users.models import User

CHARS = '1234567890'

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'users/home.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = ''
        for i in range(10):
            token += random.choice(CHARS)
        form.verified_pass = token
        user = form.save()
        user.token = token
        send_mail(
            subject='Верификация почты',
            message=f'Поздравляем с регистрацией в сервисе KnowlegeHub \n'
                    f'Для завершения регистрации введите код подтверждения в открывшемся окне: \n'
                    f'{user.token} \n'
                    f'Если вы не причастны к регистации - игнорируйте это письмо.\n'
                    f'С Уважением, команда KnowlegeHub',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

