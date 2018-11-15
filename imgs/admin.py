from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Menu, Org, UserProfile, Certificate


# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('text', 'iconCls', 'checked', 'url', 'parentMenu', 'seq')


@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('org', 'bookedDate', 'sn', 'attachmentNo', 'uploaderName')


# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('code', 'name')


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'username', 'org')

# admin.site.register(UserProfile)
