from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from newsly.news.models import DiscordWebhookStore

admin.site.register(CustomUser, UserAdmin)
