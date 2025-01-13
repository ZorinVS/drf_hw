import copy

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from lms.paginators import PageNumberPagination
from lms.validators import LEGAL_RESOURCES
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        """ Подготовка данных для тестов """
        self.total_lessons_count = 7  # общее количество уроков для тестов
        self.api_test_lessons_count = 2  # количество уроков для тестирования API

        # Атрибуты для хранения объектов
        self.user = User.objects.create(email='user@test.com')
        self.new_user = User.objects.create(email='new_user@test.com')
        self.moderator_user = User.objects.create(email='moderator@test.com')
        self.course = Course.objects.create(name='Test Course', description='Test Course Description', owner=self.user)
        self.lessons = []

        # Создание группы "moderators"
        self.moderator_group = Group.objects.create(name='moderators')
        self.moderator_user.groups.add(self.moderator_group)

        # Данные для тестирования
        self.db_data = []
        self.data_for_api = []

        # Создание уроков и подготовка данных для тестов
        data_for_orm = [
            {
                'name': f'Test Lesson{number}',
                'description': f'Test Lesson{number} Description',
                'link': f'https://youtube.com/lesson{number}',
            } for number in range(1, self.total_lessons_count + 1)
        ]

        for i, lesson_data in enumerate(data_for_orm):
            api_data: dict[str, any] = copy.deepcopy(lesson_data)
            api_data.update({'course': [self.course.pk]})
            self.data_for_api.append(api_data)

            db_data = copy.deepcopy(api_data)
            db_data.update({'owner': self.user.pk})
            self.db_data.append(db_data)

            if i < self.total_lessons_count - self.api_test_lessons_count:
                lesson = Lesson.objects.create(**lesson_data, owner=self.user)
                lesson.course.add(self.course)
                self.lessons.append(lesson)

    @staticmethod
    def select_data_for_comparison(result, expected, keys=('name', 'owner', 'link', 'course')):
        """ Выборка данных по ключам для сравнения в методе assertEqual """

        first, second = ([data[key] for key in keys] for data in [result, expected])
        return {'first': first, 'second': second}

    def test_create_lesson(self):
        """ Тест создания уроков """
        url = reverse('lms:lessons-create')

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.post(url, data=self.data_for_api[0])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест авторизованным пользователем ===
        self.client.force_authenticate(user=self.user)
        # №1 – успешное создание урока
        response = self.client.post(url, data=self.data_for_api[-2])  # тест с предпоследним элементом данных
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            **self.select_data_for_comparison(
                result=response.json(),
                expected=self.db_data[-2],
            )
        )
        # №2 – использование ссылки на сторонний ресурс
        illegal_data = copy.deepcopy(self.data_for_api[-1])  # тест с последним измененным элементом данных
        illegal_data.update({'link': illegal_data['link'].replace('youtube', 'pornhub')})
        response = self.client.post(url, data=illegal_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(
            response.json()['non_field_errors'][0],
            f'Разрешены ссылки только на следующие ресурсы: {", ".join(LEGAL_RESOURCES)}'
        )
        # №3 – создание урока, который был уже создан
        response = self.client.post(url, data=self.data_for_api[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # === 3. Тест модератором ===
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.post(url, data=self.data_for_api[-1])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.',
        )

    def test_retrieve_lesson(self):
        """ Тест просмотра детальной информации урока """
        url = reverse('lms:lessons-get', args=(self.lessons[0].pk,))

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест владельцем и модератором ===
        for user in {self.user, self.moderator_user}:
            self.client.force_authenticate(user=user)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                **self.select_data_for_comparison(
                    result=response.json(),
                    expected=self.db_data[0],
                )
            )

        # === 3. Тест новым пользователем, который еще ничего не купил и не создал ===
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.',
        )

    def test_list_lesson(self):
        """ Тест получения списка уроков """
        url = reverse('lms:lessons-list')

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест владельцем и модератором ===
        for user in {self.user, self.moderator_user}:
            self.client.force_authenticate(user=user)
            response = self.client.get(url)
            result = response.json()
            lessons_count = self.total_lessons_count - self.api_test_lessons_count
            expected = {
                'count': lessons_count,
                'next': 'http://testserver/lessons/?page=2' if lessons_count > PageNumberPagination.page_size else None,
                'previous': None,
                'results': []
            }
            result_list = []
            for i, res_data in enumerate(result['results']):
                res_dict = self.select_data_for_comparison(res_data, self.db_data[i])
                result_list.append(res_dict['first'])
                expected['results'].append(res_dict['second'])
            result['results'] = result_list
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(result, expected)

        # === 3. Тест новым пользователем, который еще ничего не купил и не создал ===
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [])

    def test_update_lesson(self):
        """ Тест обновления урока """
        url = reverse('lms:lessons-update', args=(self.lessons[0].pk,))
        new_data = {'name': 'New Test Lesson'}

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест владельцем и модератором ===
        for user in {self.user, self.moderator_user}:
            self.client.force_authenticate(user=user)
            response = self.client.patch(url, data=new_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                first=response.json()['name'],
                second=new_data['name'],
            )

        # === 3. Тест новым пользователем, который еще ничего не купил и не создал ===
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson(self):
        """ Тест удаления урока """
        delete_url = reverse('lms:lessons-delete', args=(self.lessons[0].pk,))
        retrieve_url = reverse('lms:lessons-get', args=(self.lessons[0].pk,))

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест обычным пользователем и модератором ===
        for user in {self.new_user, self.moderator_user}:
            self.client.force_authenticate(user=user)
            response = self.client.delete(delete_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # === 3. Тест владельцем ===
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(retrieve_url)  # проверка наличия после удаления
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        """ Подготовка данных для тестов """

        subscribed_data = {'name': 'Subscribed Course', 'description': 'Subscribed Course Description'}
        unsubscribed_data = {'name': 'Unsubscribed Course', 'description': 'Unsubscribed Course Description'}

        self.user = User.objects.create(email='user@test.com')
        self.subscribed_course = Course.objects.create(**subscribed_data, owner=self.user)
        self.unsubscribed_course = Course.objects.create(**unsubscribed_data, owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.subscribed_course)
        self.subscription_url = reverse('lms:subscription')

        self.data_for_api = (
            {'course': self.unsubscribed_course.pk},
            {'course': self.subscribed_course.pk},
        )

    def get_course_details(self, pk):
        """ Получение ответа запроса детальной информации курса """
        url = reverse('lms:course-detail', args=(pk,))
        self.client.force_authenticate(user=self.user)
        return self.client.get(url)

    @staticmethod
    def get_subscription_status(response):
        """ Получение значения подписки из API ответа """
        return response.json()['is_subscribed']

    def test_subscription(self):
        """ Тест подписки на курс """

        # Получение pk курса, на который пользователь еще не подписан
        pk = self.unsubscribed_course.pk

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.post(self.subscription_url, data=self.data_for_api[0])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест авторизованным пользователем ===
        response = self.get_course_details(pk)  # статус подписки перед началом теста
        self.assertEqual(self.get_subscription_status(response), False)

        response = self.client.post(self.subscription_url, data=self.data_for_api[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'подписка добавлена')

        response = self.get_course_details(pk)  # статус подписки после выполнения теста
        self.assertEqual(self.get_subscription_status(response), True)

    def test_unsubscribe(self):
        """ Тест на отмену подписки на курс """

        # Получение pk курса, на который пользователь уже подписан
        pk = self.subscribed_course.pk

        # === 1. Тест неавторизованным пользователем ===
        response = self.client.post(self.subscription_url, data=self.data_for_api[1])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # === 2. Тест авторизованным пользователем ===
        response = self.get_course_details(pk)  # статус подписки перед началом теста
        self.assertEqual(self.get_subscription_status(response), True)

        response = self.client.post(self.subscription_url, data=self.data_for_api[1])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'подписка удалена')

        response = self.get_course_details(pk)  # статус подписки после выполнения теста
        self.assertEqual(self.get_subscription_status(response), False)
