from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(GenericViewSet, ListModelMixin):
    queryset = News.objects.all().order_by('-created')
    serializer_class = NewsSerializer
