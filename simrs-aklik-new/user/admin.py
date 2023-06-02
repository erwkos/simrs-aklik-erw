from django.contrib import admin

from .models import User, UserRole


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass
