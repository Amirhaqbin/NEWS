from rest_framework import serializers
from .models import NewsPage, Comment, OtpRequest
from django.dispatch import receiver
from django.db import models
from rest_framework import serializers

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
                'view_count',
                'slug'
            )
            read_only_fields = (
                'rate',
                'view_count',
                'id',
                'slug'
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


class OtpRequestSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices= OtpRequest.OtpChannel.choices)

class OtpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpRequest
        fields = ['request_id']

class VerfyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)

class ObtainTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()