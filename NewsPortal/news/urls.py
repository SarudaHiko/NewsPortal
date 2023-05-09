from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('article/create/', PostCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
