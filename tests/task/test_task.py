from django.test import TestCase
from django.contrib.auth import get_user_model
from src.task.models import Task, TierStatus


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            telegram_username='@username1'
        )
        self.task = Task.objects.create(
            name='Test Task',
            task_condition='Some task condition.',
            description='Some task description',
            points=10,
            tier=TierStatus.EASY,
            temp_answer='correct_answer'
        )

    def test_task_creation(self):
        task = Task.objects.get(name='Test Task')
        self.assertEqual(task.task_condition, 'Some task condition.')
        self.assertEqual(task.description, 'Some task description')
        self.assertEqual(task.points, 10)
        self.assertEqual(task.min_points, 1)
        self.assertEqual(task.temp_answer, '')
        self.assertEqual(task.tier, TierStatus.EASY)
        self.assertTrue(task.is_correct_answer('correct_answer'))
        self.assertFalse(task.is_correct_answer('incorrect_answer'))

    def test_task_save(self):
        self.assertEqual(self.task.temp_answer, '')
        self.assertTrue(self.task.is_correct_answer('correct_answer'))
        self.assertEqual(self.task.temp_answer, '')
        self.task.save()
        self.assertEqual(self.task.temp_answer, '')
        self.assertTrue(self.task.is_correct_answer('correct_answer'))
        self.assertNotEqual(self.task.answer, 'test_answer')

    def test_task_absolute_url(self):
        url = self.task.get_absolute_url()
        self.assertEqual(url, f'/task/{self.task.pk}')
