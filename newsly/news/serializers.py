from rest_framework import serializers

from .models import News, Category, Tag
from newsly.accounts.models import CustomUser


class UserAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    description_text = serializers.ReadOnlyField()

    class Meta:
        model = Category
        exclude = ['description']


class TagSerializer(serializers.ModelSerializer):
    description_text = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        exclude = ['description']


class NewsSerializer(serializers.ModelSerializer):
    body_text = serializers.ReadOnlyField()

    author = UserAuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = News
        exclude = ['body']
