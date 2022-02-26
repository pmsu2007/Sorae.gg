from django import forms
from community.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content', 'type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']