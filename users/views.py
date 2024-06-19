import random

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView

from config import settings
from users.forms import UserRegisterForm
from users.models import User

CHARS = '1234567890'

# Create your views here.


class HomePageView(TemplateView):
    model = User
    template_name = 'users/home.html'
    context_object_name = 'user'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('homepage:homepage')

    def form_valid(self, form):
        token = ''
        for i in range(5):
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


class OTPConfirmView(View):
    template_name = 'users/otp_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        otp_code = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        print(user_id)

        try:
            user = User.objects.get(id=user_id)
            if user.token == otp_code:
                user.is_verified = True
                user.save()
                return HttpResponseRedirect(reverse('users:login'))
            else:
                return render(request, self.template_name, {'error': 'Неверный код подтверждения'})
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'Пользователь не существует'})


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    context_object_name = 'user'
    template_name = 'users/user_login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return self.render_to_response(self.get_context_data(form=form))
