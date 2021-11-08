from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes= models.ManyToManyField(User,related_name='blog_post',null=True,blank=True)
    dislikes=models.ManyToManyField(User,related_name='dislikes',null=True,blank=True)
    image= models.ImageField(blank= True, upload_to='Posts_images')
    comments= models.ManyToManyField(User,through='Comment',null=True,blank=True,related_name="Post_comments")

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
          # to return the absolute url of the last created post and give it to the view class . 

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes= models.ManyToManyField(User,related_name='comment_likes',null=True,blank=True)
    dislikes=models.ManyToManyField(User,related_name='comment_dislikes',null=True,blank=True)
    def __str__(self):
        return f"{self.author} : {self.body}"