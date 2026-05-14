from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
        
        
class FollowingSystem(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        indexes = [
            models.Index(fields=['from_user', 'to_user']),
        ]
    
    def __str__(self):
        return f'{self.from_user.username} follows {self.to_user.username}'
    
    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("You can not follow yourself :)...")