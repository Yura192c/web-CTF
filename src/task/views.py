from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskAnswerForm
# Create your views here.


from django.shortcuts import get_object_or_404
from .models import Task, Solution
from django.contrib.auth.decorators import login_required


@login_required
def tasks_list(request):
    # Получаем текущего пользователя
    user = request.user
    if user.is_superuser:
        solved_tasks = []
    else:
        # Получаем список решенных задач пользователем
        solved_tasks = Solution.objects.filter(user=user).values_list('task', flat=True)

    # Фильтруем задачи по уровням сложности и исключаем решенные задачи
    tier_easy = Task.objects.filter(tier='C').exclude(id__in=solved_tasks).only('id', 'name', 'points')
    tier_medium = Task.objects.filter(tier='B').exclude(id__in=solved_tasks).only('id', 'name', 'points')
    tier_hard = Task.objects.filter(tier='A').exclude(id__in=solved_tasks).only('id', 'name', 'points')

    return render(request, 'tasks_list.html', {
        'tier_easy': tier_easy,
        'tier_medium': tier_medium,
        'tier_hard': tier_hard
    })


@login_required
def task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        form = TaskAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            # Вызываем метод is_correct_answer и проверяем правильность ответа
            is_correct = task.is_correct_answer(user_answer)

            # Ваша логика для обработки правильного или неправильного ответа
            if is_correct:
                # Предполагаем, что у вас есть текущий пользователь
                user = request.user

                # Создаем объект Solution
                solution = Solution.objects.create(user=user, task=task, points_earned=task.points)
                print('*' * 10, task.id)
                return redirect('task_list')
            else:
                form = TaskAnswerForm()
                return render(request, 'task_detail.html', {'task': task, 'form': form, 'status': 'uncorrect_answer'})

    else:
        form = TaskAnswerForm()

    return render(request, 'task_detail.html', {'task': task, 'form': form})
