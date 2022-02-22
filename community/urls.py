from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'community'

urlpatterns = [
    path('', views.list, name='list'), # sorae.gg/community/ (list)
    path('<int:post_id>/', views.detail, name='detail'), # sorae.gg/community/post_id
    path('editor/', views.post_editor, name='editor'), # sorae.gg/community/editor
    path('comment/editor/<int:post_id>/', views.comment_create, name='comment_create'),
]