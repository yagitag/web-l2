from django.db import models
from django.contrib.auth.models import User


class UserCreation(models.Model):
  author = models.ForeignKey('auth.User')
  title = models.CharField(max_length=128)
  date = models.DateTimeField(auto_now_add=True, blank=True)
  content = models.CharField(max_length=2**13)
  likes_cnt = models.IntegerField(default=0)


class Post(UserCreation):
  preview_char_cnt = models.IntegerField(default=0)
  def preview(self):
    return self.content[:self.preview_char_cnt]


class Comment(UserCreation):
  post = models.ForeignKey('Post')
  parent = models.ForeignKey('self', blank=True, null=True)



class Tag(models.Model):
  post = models.ForeignKey('Post')
  value = models.CharField(max_length=32)


class Like(models.Model):
  creation = models.ForeignKey('UserCreation')
  author = models.ForeignKey('auth.User')
  is_positive = models.BooleanField()
