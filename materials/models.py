from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


# Create your models here.


class EducationModule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Название", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    preview = models.ImageField(upload_to='materials/module_preview', verbose_name="Превью", **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.owner}'

    class Meta:
        verbose_name = "Образовательный модуль"
        verbose_name_plural = "Образовательные модули"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='materials/lessons_preview/', verbose_name='Превью урока', **NULLABLE)
    URL = models.URLField(verbose_name='URL')
    education_module = models.ForeignKey(EducationModule, on_delete=models.CASCADE, verbose_name='Курс',
                                         **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.URL} {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-title', ]


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Подписчик', on_delete=models.CASCADE)
    module = models.ForeignKey(EducationModule, verbose_name='Курс', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course} - {self.user}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
