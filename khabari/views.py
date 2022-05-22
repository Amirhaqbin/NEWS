from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import NewsPageSerializer, CommentSerializer, VerfyOtpRequestSerializer,OtpResponseSerializer, OtpRequestSerializer, ObtainTokenSerializer
from .models import NewsPage, Comment, NewsLike, OtpRequest
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone

class LogoutAPIView(GenericAPIView):
    permission_class = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f"{request.user.username} بدرور "})


class VideosListView(APIView):
    def get (self, request):
        data = NewsPage.objects.filter(has_video=True)
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)

class TodaysNewsListView(APIView):
    def get (self, request):
        today = timezone.now().replace(hour=00, minute=00, second=00)
        data = NewsPage.objects.filter(created_at__gte = today)
        print(f'============== {today}')
        print(f'============== {data}')
        data2 = NewsPage.objects.all()
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)
    

class ImportantNewsListView(APIView):
    def get (self, request):
        data = NewsPage.objects.filter(important = True)
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)

class popularNewsListView(APIView):
    def get (self, request):
        data = NewsPage.objects.order_by('-like')
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)

class NewestNewsListView(APIView):
    def get (self, request):
        data = NewsPage.objects.order_by('-created_at')
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)


class MostViewsNewsListView(APIView):
    def get (self, request):
        data = NewsPage.objects.order_by('-view_count')
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)


class NewsPageViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = NewsPageSerializer
    queryset = NewsPage.objects.all()
    filterset_fields = ['title', 'author', 'like']
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        object.view_count = object.view_count + 1
        object.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)


class RecommendedNewsListView(APIView):
    def get (self, request):
        data = NewsPage.objects.filter(recommended=True)
        serializer = NewsPageSerializer(data, many=True)
        return Response(serializer.data)

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

class Register(APIView):
    pass


class OtpView(APIView):
    def get(self, request):
        serializer = OtpRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try: 
                otp = OtpRequest.objects.generate(data)
                return Response(data=OtpResponseSerializer(otp).data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data= serializer.errors)

    def post(self, request):
        serializer = VerfyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OtpRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                return Response(self._handel_login(data))
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


    def _handel_login(self, otp):
        # User = get_user_model()
        query = User.objects.filter(username=otp['receiver'])
        if query.exists():
            created = False
            user = query.get()
        else:
            user= User.objects.create(username=otp['receiver'])
            created = True
    
        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
            'created': created
            }).data




        