from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse


class TierStatus(models.TextChoices):
    HARD = 'A', 'Сложная'
    MEDIUM = 'B', 'Средняя'
    EASY = 'C', 'Легкая'


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    task_condition = models.CharField(max_length=500)
    file = models.FileField(null=True, blank=True, )
    description = models.TextField(max_length=1000, null=True, blank=True)
    points = models.PositiveIntegerField(help_text="Актуальное количество очков за решение задачи")
    min_points = models.PositiveIntegerField(help_text="Минимально очков за решение задачи", default=1)
    url = models.URLField(null=True, blank=True)
    tier = models.CharField(max_length=100, choices=TierStatus.choices,
                            default=TierStatus.EASY, help_text='Уровень сложности задачи')
    answer = models.CharField(null=False, blank=False,
                              max_length=500, editable=False)
    temp_answer = models.CharField(null=False, blank=False, max_length=500)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.answer = make_password(self.temp_answer)
            self.temp_answer = ""
        super().save(*args, **kwargs)

    def is_correct_answer(self, answer):
        return check_password(answer, self.answer)


class Solution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date_solved = models.DateTimeField(
        auto_now_add=True)  # Дата и время решения задачи
    points_earned = models.PositiveIntegerField()  # Количество полученных очков

    def __str__(self):
        return f"{self.user.username} - {self.task.name} - {self.date_solved}"

    def save(self, *args, **kwargs):
        # При сохранении решения, уменьшаем количество максимальных очков для задачи
        self.user.points_count += self.task.points
        self.points_earned = self.task.points
        if self.task.tier not in ['C']:
            if (self.task.points - 5) >= self.task.min_points:
                self.task.points -= 5
                self.task.save()
        self.user.tasks_count += 1
        self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'task')
