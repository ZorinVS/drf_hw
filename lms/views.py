from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms import services
from lms.models import Course, Lesson, Subscription
from lms.paginators import PageNumberPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.tasks import send_update_notifications
from users.permissions import IsModeratorUser, IsOwnerUser, IsStudentUser


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        last_update = self.get_object().updated_at
        course = serializer.save()

        is_subscribed = course.subscriptions.exists()
        if is_subscribed and services.has_time_passed_since_update(last_update):
            send_update_notifications(updated_course=course)

        else:
            reason = 'Прошло меньше 4 часов с последнего обновления' if is_subscribed else 'Нет подписчиков на курс'
            print(f'Уведомления не были разосланы! Причина: {reason}')

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModeratorUser]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwnerUser | IsStudentUser | IsModeratorUser]
        elif self.action in {'update', 'partial_update'}:
            self.permission_classes = [IsAuthenticated, IsOwnerUser | IsModeratorUser]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwnerUser]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        return services.get_product_queryset(
            user=self.request.user,
            model=Course,
        )


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsModeratorUser]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return services.get_product_queryset(
            user=self.request.user,
            model=Lesson,
        )


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerUser | IsStudentUser | IsModeratorUser]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerUser | IsModeratorUser]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerUser]
    queryset = Lesson.objects.all()


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=SubscriptionSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = generics.get_object_or_404(Course.objects.all(), pk=course_id)
        subs_item = course_item.subscriptions.filter(user=user)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
