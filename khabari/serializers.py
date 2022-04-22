from rest_framework import serializers
from .models import NewsPage, Comment


class NewsPageSerializer(serializers.ModelSerializer):
    class Meta:
            model = NewsPage
            fields = (
                'id',
                'title',
                'author',
                'genre',
                'news_image',
                'news_text',
                'like',
                'published_at',
                'view_count'
            )
            read_only_fields = (
                'rate',
                'view_count',
                'id'
            )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'news',
            'text',
            'rating'
        )
        read_only_fields = (
            'user',
            'id'
            )

    def create(self, validated_data):
        user = self.context['user']
        validated_data["user"] = user
        instance = super().create(validated_data)
        return instance