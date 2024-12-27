from django.core.management import BaseCommand, call_command

from lms.models import Lesson, Course
from users.models import User

FIXTURE_PATHS = (
    'courses_fixture.json',
    'lessons_fixture.json',
    'users_fixture.json',
    'payment_fixture.json',
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Очистка перед загрузкой данных
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        # Загрузка данных
        for fixture_path in FIXTURE_PATHS:
            call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))
        self.stdout.write(
            'Данные администратора:\n'
            '    - email: admin@admin.com\n'
            '    - password: 123'
        )
