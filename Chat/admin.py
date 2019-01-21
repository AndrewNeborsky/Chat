from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Chat.models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
