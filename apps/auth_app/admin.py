from django.contrib import admin

from apps.auth_app.models import AuthUser

# Register your models here.
admin.site.register(AuthUser)
