from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=50)
    slug = models.CharField(max_length=80)
    timeStamp = models.DateTimeField(default=now)


    def __str__(self):
        return self.title



class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)


    def __str__(self):
        return f'{self.comment[0:13]} .... by {self.user.username} '
    