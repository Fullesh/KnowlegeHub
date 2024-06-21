from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class HomepageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@service.py')
        self.user.set_password('1')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_homepageview(self):
        url = reverse('homepage:homepage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

