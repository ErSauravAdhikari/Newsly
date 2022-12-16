from django.contrib import messages

from django.contrib import admin
from django_q.tasks import async_task

from .helpers import send_news_in_discord
from .models import Category, Tag, News, NewsInteraction, RelevantNews, DiscordWebhookStore

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(DiscordWebhookStore)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_draft')

    @admin.action(description="Only | Generate Relevancy")
    def generate_relevancy(self, request, queryset):
        for news in queryset:
            async_task(news.generate_relevancy)

    # All self by default are draft and this action is used to publish those draft to production
    @admin.action(description="Publish")
    def publish_news(self, request, queryset):
        for news in queryset:
            news.is_draft = False
            news.save()

    @admin.action(description="Only | Summary TTS")
    def generate_summary_tts(self, request, queryset):
        for news in queryset:
            async_task(news.get_tts_summary)

        self.message_user(request, f"Background Task established to generate Summary TTS.", messages.SUCCESS)

    @admin.action(description="Only | Full TTS")
    def generate_full_tts(self, request, queryset):
        for news in queryset:
            async_task(news.get_tts_body)

        self.message_user(request, f"Background Task established to generate Full News TTS.", messages.SUCCESS)

    @admin.action(description="Only | Generate Summary")
    def admin_generate_summary(self, request, queryset):
        for news in queryset:
            async_task(news.generate_summary)

        self.message_user(request, f"Background Task established to generate Summary.", messages.SUCCESS)

    @admin.action(description="Process")
    def process_news(self, request, queryset):
        for news in queryset:
            async_task(news.process_news)

        self.message_user(request, f"Processing has been initialized.", messages.SUCCESS)

    actions = [publish_news, process_news, generate_relevancy, generate_summary_tts, generate_full_tts,
               admin_generate_summary]


admin.site.register(News, NewsAdmin)

admin.site.register(NewsInteraction)
admin.site.register(RelevantNews)
