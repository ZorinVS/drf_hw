from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from users.models import User

# Разрешенное количество неактивных дней
LAST_LOGIN_LIMIT = timedelta(days=30)


@shared_task
def disable_inactive_users():
    """ Блокировка пользователей ресурса, которые не входили в систему более месяца """

    # print('Вызов disable_inactive_users()')
    inactive_users = User.objects.filter(
        is_active=True,
        is_superuser=False,
        is_staff=False,
        last_login__lt=timezone.now() - LAST_LOGIN_LIMIT
    ).exclude(groups__name='moderators')

    if inactive_users.exists():
        email_list = [user.email for user in inactive_users]
        inactive_users.update(is_active=False)  # блокировка пользователей
        print(f"Заблокированы следующие пользователи: {', '.join(email_list)}")
