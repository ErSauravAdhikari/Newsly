from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import News, Category, Tag, NewsInteraction, DiscordWebhookStore
from ..accounts.models import CustomUser


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
    created_str = serializers.ReadOnlyField()

    comma_separate_tags = serializers.ReadOnlyField()

    class Meta:
        model = News
        exclude = ['body', 'author', 'category', 'tags', 'metadata', 'is_draft']


class NewsInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsInteraction
        fields = ['news', 'user']


class DiscordWebhookSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=CustomUser.objects.all(),
        validators=[UniqueValidator(queryset=DiscordWebhookStore.objects.all())]
     )

    class Meta:
        model = DiscordWebhookStore
        fields = ['user', 'webhook']