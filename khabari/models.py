from django.db import models
from django.contrib.auth.models import User

class NewsPage(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    ratings = models.ManyToManyField(User, blank=True, through='NewsRating')
    rate = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='library/static/covers/', default='static/covers/default-cover.jpeg')
    view_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class NewsRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPage, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    class Meta:
        unique_together = ('user', 'news')

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPage, related_name='comments', on_delete=models.CASCADE)
    message = models.TextField()