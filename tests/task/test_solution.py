from django.test import TestCase
from django.contrib.auth import get_user_model
from src.task.models import Task, Solution, TierStatus


class SolutionModelTest(TestCase):
    def test_solution_creation(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            telegram_username='@username1'
        )
        task = Task.objects.create(
            name='Test Task',
            task_condition='Some task condition.',
            description='Some task description',
            points=10,
            tier=TierStatus.EASY,
            temp_answer='correct_answer'
        )

        solution = Solution.objects.create(
            user=user,
            task=task,
            points_earned=task.points
        )
        self.assertEqual(solution.user, user)
        self.assertEqual(solution.task, task)
        self.assertEqual(solution.points_earned, 10)

    def test_solution_save(self):
        user = get_user_model().objects.create_user(
            username='testuser2',
            password='testpassword2',
            telegram_username='@username2'
        )
        task = Task.objects.create(
            name='Test Task',
            task_condition='Some task condition.',
            points=55,
            min_points=50,
            tier=TierStatus.HARD,
            temp_answer='correct_answer'
        )

        initial_user_points_count = user.points_count
        initial_user_tasks_count = user.tasks_count

        solution = Solution.objects.create(
            user=user,
            task=task,
        )

        self.assertEqual(user.points_count,
                         initial_user_points_count+task.points + 5)
        self.assertEqual(user.tasks_count, initial_user_tasks_count + 1)
        self.assertEqual(solution.points_earned, task.points + 5)
        self.assertEqual(task.points, 50)

        
