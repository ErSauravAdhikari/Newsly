from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from newsly.news.api import NewsViewSet, NewsInteractionViewSet, FilterNewsViewSet, DiscordWebhookView
from newsly.news.views import email_example, trigger_relevancy

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'interactions', NewsInteractionViewSet)
router.register(r'relevant-news', FilterNewsViewSet, basename='News')
router.register(r'user/webhook', DiscordWebhookView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('summernote/', include('django_summernote.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('demo', email_example),
    path('relevancy-trigger/', trigger_relevancy),
    path('', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
