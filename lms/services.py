from django.db import models as db_models

from lms.models import Course, Lesson

PRODUCT_MODELS = {Course, Lesson}


def get_product_queryset(user, model):
    """ Получение QuerySet продуктов для авторизованных пользователей """

    if model not in PRODUCT_MODELS:
        supported_models = ', '.join(m.__name__ for m in PRODUCT_MODELS)
        raise ValueError(f'Переданный объект не является поддерживаемой моделью. Ожидаются: {supported_models}')

    # QuerySet для модератора
    if user.groups.filter(name='moderators').exists():
        return model.objects.all()
    # QuerySet для автора и студента
    return model.objects.filter(
        db_models.Q(owner=user) | db_models.Q(payments__user=user)
    ).distinct()
