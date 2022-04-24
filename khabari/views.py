from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import NewsPageSerializer, CommentSerializer
from .models import NewsPage, Comment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class LogoutAPIView(GenericAPIView):
    permission_class = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f"{request.user.username} بدرور "})


class NewsPageViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = NewsPageSerializer
    queryset = NewsPage.objects.all()
    filterset_fields = ['title', 'genre', 'author', 'like']

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        object.view_count = object.view_count + 1
        object.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)


class CommentViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['user', 'news']

    def get_serializer_context(self):
        context = super(CommentViewset, self).get_serializer_context()
        context['user'] = self.request.user
        return context
