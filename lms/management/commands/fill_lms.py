from django.contrib.auth.models import Group
from django.core.management import BaseCommand, call_command

from lms.models import Lesson, Course
from users.models import User

FIXTURE_PATHS = (
    'users/fixtures/groups_fixture.json',
    'users/fixtures/users_fixture.json',
    'lms/fixtures/courses_fixture.json',
    'lms/fixtures/lessons_fixture.json',
    'users/fixtures/payment_fixture.json',
)

AUTH_DETAILS = ("""
Данные администратора:
    - email: admin@admin.com
    - password: 123

Данные пользователей:
  Модераторы:
    - moderator1@example.com
  Авторы:
    - author1@example.com
    - author2@example.com
  Студенты:
    - student1@example.com
    - student2@example.com
  Новый пользователь (без курсов/уроков):
    - new_user@example.com
  Пароль для пользователей: password123
""")


class Command(BaseCommand):
    help = 'Наполнение проекта тестовыми данными с выводом данных для авторизации'

    def handle(self, *args, **options):
        # Очистка перед загрузкой данных
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()

        # Загрузка данных
        for fixture_path in FIXTURE_PATHS:
            call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))

        # Вывод данных для авторизации
        self.stdout.write(AUTH_DETAILS)
