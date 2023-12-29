from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            telegram_username='@username1',
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.points_count, 0)
        self.assertEqual(user.tasks_count, 0)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            username='adminuser',
            telegram_username='@username1',
            password='adminpassword'
            
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_telegram_username_format(self):
        # Проверка правильного формата
        valid_user = get_user_model().objects.create_user(
            username='testuser',

            password='testpassword',
            telegram_username='@username1'
        )
        self.assertEqual(valid_user.telegram_username, '@username1')

        # Проверка неправильного формата
        with self.assertRaises(ValueError):
            invalid_user = get_user_model().objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpassword',
                telegram_username='invalidusername'
            )

    def test_allowed_telegram_usernames(self):
        with self.assertRaises(ValueError):
            invalid_user = get_user_model().objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpassword',
                telegram_username='@invalidusername'
            )
