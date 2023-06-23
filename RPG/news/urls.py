from django.urls import path
from django.views.generic import ListView
from .models import Post
from .views import PostList, PostCreate, PostDetail, PostUpdate, PostDelete, author_posts


urlpatterns = [
    path('',(PostList.as_view()), name = 'post_list'),
    path('create/', PostCreate.as_view(), name = 'post_create'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('author/posts/', author_posts, name='author_posts'),  # Проверка, что статьи получены

]
