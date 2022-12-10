from django.contrib import messages

from django.contrib import admin
from django_q.tasks import async_task

from .models import Category, Tag, News

admin.site.register(Category)
admin.site.register(Tag)


class NewsAdmin(admin.ModelAdmin):
    @admin.action(description="Summary TTS")
    def generate_summary_tts(self, request, queryset):
        for news in queryset:
            async_task(news.get_tts_summary)

        self.message_user(request, f"Background Task established to generate Summary TTS.", messages.SUCCESS)

    @admin.action(description="Full TTS")
    def generate_full_tts(self, request, queryset):
        for news in queryset:
            async_task(news.get_tts_body)

        self.message_user(request, f"Background Task established to generate Full News TTS.", messages.SUCCESS)

    actions = [generate_summary_tts, generate_full_tts]


admin.site.register(News, NewsAdmin)
