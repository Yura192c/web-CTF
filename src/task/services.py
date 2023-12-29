from src.user.models import User


def get_users_with_solved_tasks():
    all_users = User.objects.all()
    return all_users
