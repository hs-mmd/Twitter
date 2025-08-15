from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from members.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("home")
    


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='likes')
    image = models.ImageField(null=True,blank=True ,upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.author}'
    
    def get_absolute_url(self):
        return reverse('home')
    
    def total_likes(self):
        return self.like.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    
    def get_absolute_url(self):
        return reverse("post_detail", args=[self.post.pk] )
     
class CategorySubscription(models.Model):
    user     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='category_subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.user.username} subscribes to {self.category.name}"
    