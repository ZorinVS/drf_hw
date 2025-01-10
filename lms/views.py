from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms import services
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorUser, IsOwnerUser, IsStudentUser


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
