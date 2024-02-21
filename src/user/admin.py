from django.contrib import admin
from .models import User, AuthorizedUsers

admin.site.register(User)
admin.site.register(AuthorizedUsers)
