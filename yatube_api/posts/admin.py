from django.contrib import admin

from .models import Comment
from .models import Group
from .models import Post
from .models import Follow


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'author', 'text', 'pub_date', 'image', 'group')
    list_editable = ('group',)
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'created', 'post')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
