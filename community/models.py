from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post')
    voter = models.ManyToManyField(User, related_name='voter_post')
    category_name = models.CharField(max_length=10)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    voter = models.ManyToManyField(User, related_name='voter_comment')


class PostHits(models.Model):
    ip = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
