from django import views
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path


router = DefaultRouter()

router.register(r'news', NewsPageViewset)
router.register(r'comments', CommentViewset)


urlpatterns = router.urls + [

    path('login/', view=obtain_auth_token),
    path('logout/', LogoutAPIView.as_view())
    
    ]