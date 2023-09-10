from captcha.models import CaptchaStore
from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    pass

# @admin.register(CaptchaStore)
# class CaptchaStoreAdmin(admin.ModelAdmin):
#     pass
# @admin.register(User)
# class UserAdminTemp(admin.ModelAdmin):
#     pass


# from django.contrib.auth.admin import
