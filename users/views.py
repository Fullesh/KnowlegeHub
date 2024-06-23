import random

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

CHARS = '1234567890'

# Create your views here.


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

        try:
            user = User.objects.get(id=user_id)
            if user.token == otp_code:
                user.is_verified = True
                user.save()
                return render(request, 'users/user_confirm_success.html')
            else:
                return render(request, self.template_name, {'error': 'Неверный код подтверждения'})
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'Пользователь не существует'})


class UserDetailView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_detail.html'
    success_url = reverse_lazy('users:detail')

    def get_object(self, queryset=None):
        return self.request.user


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    context_object_name = 'user'
    template_name = 'users/user_login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete_confirm.html'
    success_url = reverse_lazy('homepage:homepage')


def res_password(request):
    new_password = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = get_object_or_404(User, email=email)
        except user.DoesNotExist:
            messages.error(request, 'Пользователя с данным E-mail не существует')
        for i in range(10):
            new_password += random.choice(CHARS)
        send_mail(
            subject='Смена пароля',
            message=f'Ваш новый пароль {new_password}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, 'users/user_password_reset.html')