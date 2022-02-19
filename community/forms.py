from django import forms
from community.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content']