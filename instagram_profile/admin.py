from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(models.Photography)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(models.Comment)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', )
