from django.db import models


class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    vote = models.SmallIntegerField()
    user_name = models.CharField(max_length=20)

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()



class User(models.Model):
    user_name = models.CharField(max_length=20)
