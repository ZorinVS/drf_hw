from celery import shared_task
from django.core.mail import send_mail

from lms.models import Course


@shared_task
def send_update_notifications(updated_course_id):
    """ Уведомление пользователей, подписанных на курс, о появлении обновлений с помощью почты """

    course = Course.objects.get(id=updated_course_id)
    emails_list = [sub.user.email for sub in course.subscriptions.all()]
    body = (f"Имеются обновления по курсу '{course.name}', "
            f"который был обновлен {course.updated_at.strftime('%d-%m-%Y %H:%M')}")

    send_mail(
        subject='Уведомление об обновлении',
        message=body,
        from_email=None,
        recipient_list=emails_list,
    )
