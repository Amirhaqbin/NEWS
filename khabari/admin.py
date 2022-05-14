from django.contrib import admin
from .models import NewsPage, Category, OtpRequest



admin.site.register(OtpRequest)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')


@admin.register(NewsPage)
class NewsPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'status')
    list_filter = ('title', 'author', 'status', 'created_at')
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'published_at'
    raw_id_field = ('author',)

