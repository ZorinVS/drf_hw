from rest_framework import serializers

LEGAL_RESOURCES = ('youtube.com',)


class AllowedResourceValidator:
    """ Валидация на отсутствие ссылок на сторонние ресурсы """

    def __init__(self, field='link'):
        self.field = field

    def __call__(self, values):
        if self.field in values:  # проверка для исключения ошибки при использовании метода patch
            user_link = values.get(self.field, '')
            if not any(resource in user_link for resource in LEGAL_RESOURCES):
                legal_resources_str = ', '.join(LEGAL_RESOURCES)
                raise serializers.ValidationError(
                    f'Разрешены ссылки только на следующие ресурсы: {legal_resources_str}'
                )
