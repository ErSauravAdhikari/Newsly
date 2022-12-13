from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from newsly.news.api import NewsViewSet, NewsInteractionViewSet, FilterNewsViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'interactions', NewsInteractionViewSet)
router.register(r'relevant-news', FilterNewsViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('summernote/', include('django_summernote.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
