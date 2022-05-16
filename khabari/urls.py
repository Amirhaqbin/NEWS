from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()

router.register(r'news', NewsPageViewset)
router.register(r'comments', CommentViewset)



urlpatterns = router.urls + [

    path('login/', view=obtain_auth_token),
    path('logout/', LogoutAPIView.as_view()),
    path('news/<slug:slug>/like', NewsLike.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('otp/', OtpView.as_view(), name='otp_view' )
    ]