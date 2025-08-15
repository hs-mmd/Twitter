from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to='profile_pics/')
    is_archived = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.user)
    
from django.db import models

class Follow(models.Model):
    follower  = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"
 
    
class FollowRequest(models.Model):
    sender   = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='sent_follow_requests')
    receiver = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='received_follow_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted   = models.BooleanField(null=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        status = 'pending' if self.accepted is None else ('accepted' if self.accepted else 'rejected')
        return f'{self.sender.user.username} → {self.receiver.user.username} ({status})'

