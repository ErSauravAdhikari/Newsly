from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny

from .models import News, NewsInteraction, RelevantNews
from .serializers import NewsSerializer, NewsInteractionSerializer
from ..accounts.models import CustomUser


class FilterNewsViewSet(GenericViewSet, ListModelMixin):
    def get_queryset(self):
        username = self.request.GET.get("username", "")
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return News.objects.none()

        queryset = News.objects.filter(is_draft=False).filter(~Q(full_body_tts="")).filter(~Q(summary_tts="")).filter(
            ~Q(summary="")).order_by('-created').filter(relevant_news__user=user).distinct()
        return queryset

    serializer_class = NewsSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = ['category', 'language']


class NewsViewSet(GenericViewSet, ListModelMixin):
    queryset = News.objects.filter(is_draft=False).filter(~Q(full_body_tts="")).filter(~Q(summary_tts="")).filter(
        ~Q(summary="")).order_by('-created')
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

    permission_classes = [AllowAny]
    filterset_fields = ['user__id']
