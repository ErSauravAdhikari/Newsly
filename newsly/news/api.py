from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(GenericViewSet, ListModelMixin):
    queryset = News.objects.filter(~Q(full_body_tts="")).filter(~Q(summary_tts="")).filter(~Q(summary="")).order_by('-created')
    serializer_class = NewsSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = ['category', 'language']
