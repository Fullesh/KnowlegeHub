from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import User
from rest_framework.test import APIClient


# Create your tests here.

class UsersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@service.py')
        self.user.set_password('1')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.token = '12345'
        self.user.save()
        self.client = APIClient()

    def test_login(self):
        url = reverse('users:login')
        data = {
            'email': 'admin@service.py',
            'password': '1'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_page_exists(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_form(self):
        url = reverse('users:register')
        data = {
            'email': 'test@service.py',
            'password1': '874218HecTorOneZero',
            'password2': '874218HecTorOneZero'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(User.objects.all().count(), 2)

    def test_register_page_exists(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_confirmation(self):
        url = reverse('users:otp_confirm')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_confirmation_send_code(self):
        url = reverse('users:otp_confirm')
        data = {
            'code': '12345'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_exists(self):
        self.client.force_login(self.user)
        url = reverse('users:detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_exists(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('users:delete', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_password_reset_exists(self):
        url = reverse('users:reset_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_password_reset(self):
        url = reverse('users:reset_password')
        data = {
            'email': 'admin@service.py'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
