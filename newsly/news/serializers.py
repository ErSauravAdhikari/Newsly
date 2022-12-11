from rest_framework import serializers

from .models import News, Category, Tag
from newsly.accounts.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['description', 'id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['description', 'id']


class NewsSerializer(serializers.ModelSerializer):
    body_text = serializers.ReadOnlyField()

    author_name = serializers.ReadOnlyField()

    all_tags = serializers.ReadOnlyField()
    category_name = serializers.ReadOnlyField()

    class Meta:
        model = News
        exclude = ['body', 'author', 'category', 'tags']
