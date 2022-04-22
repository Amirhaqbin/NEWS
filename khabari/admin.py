from django.contrib import admin
from .models import NewsPage


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'status')
    list_filter = ('title', 'author', 'status', 'created_at')
    search_fields = ['title']

admin.site.register(NewsPage, NewsAdmin)