from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models.models import Course, Lesson
from lms.models.subscription import Subscription
from users.models import CustomUser, UserRoles


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser(email='123@mail.ru',
                               phone='111111111',
                               city='Moscow',
                               is_superuser=False,
                               is_staff=False,
                               is_active=True,
                               role=UserRoles.MEMBER
                               )
        self.user.set_password('123')
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {"email": "123@mail.ru", "password": "123"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # Тестовый курс
        self.course = Course.objects.create(
            title="test_course",
            owner=self.user

        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="This is a test lesson",
            course=self.course,
            owner=self.user
        )

    def test_create_lesson(self):
        data = {
            "title": "test2",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/",
            "description": "test description",
            "owner": self.user.id
        }
        create_lesson = reverse('lesson_create')
        response = self.client.post(create_lesson, data,
                                    format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])

    def test_retrieve_lesson(self):
        retrieve_url = reverse('lesson_detail',
                               args=[self.lesson.id])
        response = self.client.get(retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        update_url = reverse('lesson_update',
                             args=[self.lesson.id])
        updated_data = {
            "title": "Updated Lesson",
            "description": "This is an updated lesson",
        }
        response = self.client.patch(update_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, updated_data['title'])
        self.assertEqual(self.lesson.description, updated_data['description'])

    def test_delete_lesson(self):
        delete_url = reverse('lesson_delete',
                             args=[self.lesson.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_list_lesson(self):
        list_url = reverse('lesson_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], self.lesson.title)


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser(email='123@mail.ru',
                               phone='111111111',
                               city='Moscow',
                               is_superuser=False,
                               is_staff=False,
                               is_active=True,
                               role=UserRoles.MEMBER
                               )
        self.user.set_password('123')
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {"email": "123@mail.ru", "password": "123"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # Тестовый курс
        self.course = Course.objects.create(
            title="test_course",
            owner=self.user

        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="This is a test lesson",
            course=self.course,
            owner=self.user
        )

    def test_list_course(self):
        course_url = reverse('course-list')
        response = self.client.get(course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], self.course.title)


class SubscriptionTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser(email='123@mail.ru',
                              phone='111111111',
                              city='Moscow',
                              is_superuser=False,
                              is_staff=False,
                              is_active=True,
                              role=UserRoles.MEMBER
                              )
        cls.user.set_password('123')
        cls.user.save()

        cls.client = APIClient()
        response = cls.client.post(
            '/api/token/',
            {"email": "123@mail.ru", "password": "123"}
        )

        cls.access_token = response.json().get('access')
        cls.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {cls.access_token}'
        )
        cls.headers = {'HTTP_AUTHORIZATION': f'Bearer {cls.access_token}'}

        cls.course = Course.objects.create(
            title="test_course",
            owner=cls.user,
        )
        cls.course2 = Course.objects.create(
            title="test_course2",
            owner=cls.user,
        )

        cls.subscribe = Subscription.objects.create(
            owner=cls.user,
            course=cls.course,
            status=False
        )

        cls.subscribe2 = Subscription.objects.create(
            owner=cls.user,
            course=cls.course2,
            status=True
        )

    def test_subscribe_to_course(self):
        subscribe_url = reverse('subscription',
                                args=[self.course.id])

        response = self.client.post(subscribe_url, {},
                                    format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Вы подписались на курс.")

    def test_unsubscribe_from_course(self):
        subscribe_url = reverse('subscription',
                                args=[self.course2.id])
        response = self.client.post(subscribe_url, {},
                                    format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Вы отписались от курса.")
