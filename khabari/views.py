from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import NewsPageSerializer, CommentSerializer
from .models import NewsPage, Comment, NewsLike
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404



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
    lookup_field = "slug"

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

class LikeAPIView(views.APIView):
    main_model = None
    like_model = None
    lookup_field = "pk"

    def set_like_field(self):
        self.like_field = str(self.obj.__class__.__name__).lower()

    @property
    def lookup_filter(self):
        return {self.lookup_field: self.kwargs[self.lookup_field]}

    @property
    def main_queryset(self):
        queryset_fields = {
            "user": self.request.user,
            self.like_field: get_object_or_404(self.main_model, **self.lookup_filter)
        }
        return queryset_fields


    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.main_model, **self.lookup_filter)
        self.set_like_field()
        if self.like_model.objects.filter(**self.main_queryset).exists():
            return Response({"liked": "True"}, status=200)
        return Response({"liked": "False"}, status=200)

    def post(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.main_model, **self.lookup_filter)
        self.set_like_field()
        if self.like_model.objects.filter(**self.main_queryset).exists():
            return Response({"detail": f"You've already liked this {self.obj.__class__.__name__}."}, status=409)
        self.like_model.objects.create(**self.main_queryset)
        return Response(status=201)

    def delete(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.main_model, **self.lookup_filter)
        self.set_like_field()
        likeobj = get_object_or_404(self.like_model, **self.main_queryset)
        likeobj.delete()
        return Response(status=204)

class NewsLike(LikeAPIView):
    main_model = NewsPage
    like_model = NewsLike
    lookup_field = "slug"