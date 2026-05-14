from django.db import models
from accounts.models import CustomUser
from autoslug import AutoSlugField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.slug
        
    def likes_count(self):
        return self.blikes.count()
        
    def user_can_like(self, user):
        user_like = user.ulikes.filter(blog=self)
        if user_like.exists():
            return False
        return True
        
        
        
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    published_from = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Commented on {self.published_from} Post"
        
        
class LikeSystem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ulikes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blikes')
    
    def __str__(self):
        return f"{self.user.username} liked {self.blog.title}"