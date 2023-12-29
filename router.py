from django.urls import path, include, re_path

urlpatterns = [
    path('', include('src.index.urls')),
    path('', include('src.task.urls')),
    path('user/', include('src.user.urls'))
]
