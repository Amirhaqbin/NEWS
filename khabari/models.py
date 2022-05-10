from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _

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
        n1 = NewsPage.objects.get(id=kwargs['id'])
        self.like = n1.like_set.all().count()
        super(NewsPage, self).save(*args, **kwargs)
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ["published_at"]


class NewsLike(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPage, related_name='likes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    news = models.ForeignKey(
        NewsPage, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    likes = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            'news',
            'user'
        )


