from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='название курса')
    preview = models.ImageField(upload_to='lms/courses/previews/', verbose_name='превью', blank=True, null=True)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses', verbose_name='владелец'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='название урока')
    course = models.ManyToManyField(Course, related_name='lessons', verbose_name='курс')
    preview = models.ImageField(upload_to='lms/lessons/previews/', verbose_name='превью', blank=True, null=True)
    description = models.TextField(verbose_name='описание')
    link = models.CharField(max_length=255, verbose_name='ссылка на видео')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons', verbose_name='владелец'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
