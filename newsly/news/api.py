from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import News, NewsInteraction
from .serializers import NewsSerializer, NewsInteractionSerializer


class NewsViewSet(GenericViewSet, ListModelMixin):
    queryset = News.objects.filter(~Q(full_body_tts="")).filter(~Q(summary_tts="")).filter(~Q(summary="")).order_by('-created')
    serializer_class = NewsSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = ['category', 'language']


class NewsInteractionViewSet(GenericViewSet, CreateModelMixin):
    queryset = NewsInteraction.objects.all()
    serializer_class = NewsInteractionSerializer
    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = ['user__id']
