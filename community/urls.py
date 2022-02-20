from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.list, name='list'), # sorae.gg/community/ (list)
    path('<int:post_id>/', views.detail, name='detail'), # sorae.gg/community/post_id
    path('comment/editor/<int:post_id>/', views.comment_create, name='comment_create'),
    path('post/editor/', views.post_create, name='post_create'),
    path('editor/', views.editor, name='editor')
    # path('login/'),
    # path('signup/'),
]