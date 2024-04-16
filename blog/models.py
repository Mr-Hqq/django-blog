from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    image=models.ImageField(upload_to='images')
    # user=models.ForeignKey(User,related_name='postuser',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    def get_post_url(self):
        return reverse('post',args=[self.pk])
    def get_addcomment_url(self):
        return reverse('addcomment',args=[self.pk])

    def __str__(self) :
        return self.title
class Comment(models.Model):
    content=models.TextField()
    email=models.EmailField()
    post=models.ForeignKey(Post,related_name='commentpost',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    def get_addreply_url(self):
        return reverse('addreply',args=[self.pk])



class Reply(models.Model):
    content=models.TextField()
    email=models.EmailField()
    comment=models.ForeignKey(Comment,related_name='replycomment',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)

