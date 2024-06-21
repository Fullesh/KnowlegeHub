from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import EducationModule, Lesson, Subscription
from users.models import User


# Create your tests here.

class EducationModuleTestCase(APITestCase):
    """
    Тестирование создания образовательного модуля
    """

    def setUp(self):
        self.user = User.objects.create(email='admin@service.py')
        self.user.set_password('1')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.Module = EducationModule.objects.create(
            name='DRF',
            description='DjangoRestFramework'
        )

    def test_education_module_create(self):
        url = reverse('materials:materials_create')
        data = {
            'name': 'DRF_Test_Module',
            'description': 'DjangoRestFramework'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EducationModule.objects.all().count(), 2)

    def test_education_module_delete(self):
        url = reverse('materials:materials_delete', kwargs={'pk': self.Module.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EducationModule.objects.all().count(), 0)

    def test_education_module_update(self):
        url = reverse('materials:materials_update', kwargs={'pk': self.Module.pk})
        new_data = {
            'description': 'UpdatedDesk'
        }
        response = self.client.patch(url, data=new_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('description'), 'UpdatedDesk')

    def test_education_module_retrieve(self):
        url = reverse('materials:materials_detail', kwargs={'pk': self.Module.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'DRF')

    def test_education_module_list(self):
        url = reverse('materials:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EducationModule.objects.all().count(), 1)


class LessonTestCase(APITestCase):
    """
    Тестирование создания образовательного модуля
    """

    def setUp(self):
        self.user = User.objects.create(email='admin@service.py')
        self.user.set_password('1')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.Lesson = Lesson.objects.create(
            title='Основы веба',
            description='DescTest',
            URL='https://youtube.com/m$keT3sT/'
        )

    def test_lesson_create(self):
        url = reverse('materials:lessons_create')
        data = {
            'title': 'Тест',
            'description': 'Тестовое описание',
            'URL': 'https://youtube.com/uue2124'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_delete(self):
        url = reverse('materials:lessons_delete', kwargs={'pk': self.Lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_update(self):
        url = reverse('materials:lessons_update', kwargs={'pk': self.Lesson.pk})
        new_data = {
            'description': 'Обновлённое описание',
            'URL': 'https://youtube.com/qq232wr'
        }
        response = self.client.patch(url, data=new_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('description'), 'Обновлённое описание')

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons_detail', kwargs={'pk': self.Lesson.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('description'), 'DescTest')

    def test_education_module_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@service.py')
        self.user.set_password('1')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.module = EducationModule.objects.create(name="Python_29")

    def test_subscribe(self):
        url = '/module/subscribe/'
        data = {
            "module": self.module.pk
        }
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Подписка включена'})

    def test_unsubscribe(self):
        url = '/module/subscribe/'
        data = {
            "module": self.module.pk
        }
        Subscription.objects.create(module=self.module, user=self.user)
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Подписка отключена'})