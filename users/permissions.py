from rest_framework import permissions

from lms.models import Course, Lesson
from users.models import Payment


class IsModeratorUser(permissions.BasePermission):
    """ Проверка на модератора """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'DELETE':
    #         return False
    #     else:
    #         return True
    #             ↓
    # актуально при удалении объекта для self.permission_classes = [IsAuthenticated, ~IsModeratorUser]


class IsOwnerUser(permissions.BasePermission):
    """ Проверка на авторство """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsStudentUser(permissions.BasePermission):
    """ Проверка на право просмотра материала: доступно пользователю, купившему курс/урок """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return Payment.objects.filter(user=request.user, paid_course=obj).exists()
        elif isinstance(obj, Lesson):
            return Payment.objects.filter(user=request.user, paid_lesson=obj).exists()
        return False


class IsProfileOwner(permissions.BasePermission):
    """ Проверка на владельца профиля """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
