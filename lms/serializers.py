from rest_framework import serializers

from lms import validators
from lms.models import Course, Lesson, Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [
            validators.AllowedResourceValidator()
        ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        return instance.subscriptions.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Course
        # fields = ('id', 'name', 'preview', 'description', 'owner', 'lesson_count', 'lessons')
        fields = ('id', 'name', 'preview', 'description', 'owner', 'is_subscribed', 'lesson_count', 'lessons')
        read_only_fields = ('owner',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                fields=['user', 'course'], queryset=Subscription.objects.all()
            )
        ]
        read_only_fields = ('user',)
