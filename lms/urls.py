from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms import views

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')


urlpatterns = [
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name='lessons-create'),
    path('lessons/', views.LessonListAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lessons-get'),
    path('lessons/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lessons-update'),
    path('lessons/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lessons-delete'),
] + router.urls
