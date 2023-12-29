from django.shortcuts import render
from src.task import services


def leaderboard(request):
    users_data = services.get_users_with_solved_tasks()
    return render(request, 'leaderboard.html', {
        'users_data': users_data
    })
