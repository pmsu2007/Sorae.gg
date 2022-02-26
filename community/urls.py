from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'community'

urlpatterns = [
    path('list/<str:category>/', views.post_list, name='list'), # sorae.gg/community/ (list)
    path('detail/<int:post_id>/', views.post_detail, name='detail'), # sorae.gg/community/post_id
    path('editor/', views.post_editor, name='editor'), # sorae.gg/community/editor
    path('<int:post_id>/editor/', views.post_modify, name='modify'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('<int:post_id>/vote/', views.post_vote, name='post_vote'),
    path('comment/<int:post_id>/editor/', views.comment_create, name='comment_create'),
    path('comment/<int:post_id>/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('comment/<int:post_id>/vote/<int:comment_id>', views.comment_vote, name='comment_vote'),
]