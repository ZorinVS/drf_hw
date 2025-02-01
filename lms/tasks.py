from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_update_notifications(updated_course):
    """ Уведомление пользователей, подписанных на курс, о появлении обновлений с помощью почты """

    emails_list = [sub.user.email for sub in updated_course.subscriptions.all()]
    body = (f"Имеются обновления по курсу '{updated_course.name}', "
            f"который был обновлен {updated_course.updated_at.strftime('%d-%m-%Y %H:%M')}")

    send_mail(
        subject='Уведомление об обновлении',
        message=body,
        from_email=None,
        recipient_list=emails_list,
    )
