from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60*1)(PostsList.as_view()), name='news'),
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
    path('article/create/', PostCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/<slug:slug>/subscribe/', subscribe_me, name='subscription'),
    path('post_limit_spent/', post_limit_spent_view, name='post_limit_spent'),
    path('mail_notify_new_post/', mail_notify_new_post_view, name='mail_notify_new_post'),
    path('weekly_notify_posts/', mail_weekly_notify_posts_view, name='mail_weekly_notify_posts'),
]
