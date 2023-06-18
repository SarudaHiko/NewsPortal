from .models import Category, Author, Post, PostCategory, Comment, Subscribers
from modeltranslation.translator import register, \
    TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('cat_name', 'slug',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('rating',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('p_type', 'title', 'time', 'text', 'rating', 'author', 'category',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('time', 'text', 'rating', 'user', 'post',)


@register(Subscribers)
class SubscribersTranslationOptions(TranslationOptions):
    fields = ('user', 'category',)
