from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['cat_name', 'slug',]


class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['p_type', 'title', 'time', 'text', 'rating', 'author', 'category',]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Author
       fields = ['rating',]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Comment
       fields = ['time', 'text', 'rating', 'user', 'post',]


class SubscribersSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Subscribers
       fields = ['user', 'category',]
