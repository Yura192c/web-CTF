from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.tasks_list, name='task_list'),
    path('task/<int:pk>', views.task, name='task_detail'),
]
