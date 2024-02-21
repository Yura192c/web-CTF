from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
]
handler404 = 'src.index.views.my_custom_page_not_found_view'
