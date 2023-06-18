from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, Subscribers
from django.contrib import admin
from modeltranslation.admin import \
    TranslationAdmin


class AuthorAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('author_acc', 'rating',)
    search_fields = ('author_acc',)
    model = Author


class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('id', 'p_type', 'title', 'author', 'text', 'rating', 'time')
    list_display_links = ('title', )
    search_fields = ('author', 'title', 'text')
    list_editable = ('p_type',)
    model = Post


class CommentAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'rating', 'time')
    list_display_links = ('text',)
    search_fields = ('user', 'text')
    list_filter = ('user', 'rating', 'time')
    model = Comment


class CategoryAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('id', 'cat_name',)
    search_fields = ('cat_name',)
    model = Category


class SubscribersAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Subscribers


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscribers, SubscribersAdmin)


