import uuid
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from datetime import timedelta
from .sender import send_otp
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class Category(models.Model):

    title = models.CharField(max_length=255)
    active = models.BooleanField()



class NewsPage(models.Model):

    STATUS_CHOICES ={
        ('Draft','draft'),
        ('Published','published')
    }

    TYPE_CHOICES = {
        ('Social','social'),
        ('Economy','economy'),
        ('Politic','politic'),
        ('Culture','culture'),
        ('Sport','sport'),
        ('Family','family'),
        ('Media','media'),
        ('Picture','picture'),
        ('International','international'),
        ('State','state'),
    }


    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    cm_likes = models.ManyToManyField(User, related_name='likes_comments', blank=True, through='Comment')
    like = models.IntegerField(default=0)
    news_text = models.TextField(blank=True, null=True)
    news_image = models.ImageField(
        upload_to='khabari/static', default='')
    video = models.FileField(
        upload_to='rename_and_path', default='')
    news_type = models.CharField(max_length=128,choices=TYPE_CHOICES, blank=True, null=True)    
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(allow_unicode=True, unique=True, null=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # n1 = NewsPage.objects.get(id=kwargs['id'])
        # self.like = n1.like_set.all().count()
        self.slug = slugify(self.title)
        super(NewsPage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ["published_at"]


"""
under this , write models for like and comment for details news and like for each comment
"""

class NewsLike(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPage, related_name='likes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    
    def save(self, *args, **kwrgs):
        self.news.like = self.news.like+1
        self.news.save()
        super().save(*args, **kwrgs)

class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='usercomments', on_delete=models.CASCADE)
    news = models.ForeignKey(
        NewsPage, related_name='newscomments', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    likes = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            'news',
            'user'
        )

"""
under this, i added otp for who first time to join app 
"""
class OtpRequestQueryset(models.QuerySet):

    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),

        ).exists()


class OtpManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQueryset(self.model, self._db)
    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)

    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp

def otp_generate():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k = 4)
    return ''.join(digits)


# class CostumeUser(AbstractUser):
#     pass


class OtpRequest(models.Model):
    class OtpChannel(models.TextChoices): 
        PHONE = 'Phone'
        EMAIL = 'E_Mail'
    request_id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    channel = models.CharField(max_length=12, blank=True, 
        choices =OtpChannel.choices, default = OtpChannel.PHONE )
    receiver = models.CharField(max_length=10)
    password = models.CharField(max_length=6, default = otp_generate)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = OtpManager()
