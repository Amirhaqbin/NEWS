from django.db import models
from django.contrib.auth.models import User

class NewsPage(models.Model):

    STATUS_CHOICES ={
        ('Draft','draft'),
        ('Published','published')
    }

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    ratings = models.ManyToManyField(User, blank=True, through='Comment')
    rate = models.FloatField(blank=True, null=True)
    news_text = models.TextField(blank=True, null=True)
    cover = models.ImageField(
        upload_to='khabari/static', default='')
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    news = models.ForeignKey(
        NewsPage, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.SmallIntegerField(
        choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    class Meta:
        unique_together = (
            'news',
            'user'
        )