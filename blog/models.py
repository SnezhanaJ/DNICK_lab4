from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    interests = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    files = models.FileField()
    blocked_users = models.ManyToManyField(User, related_name='blocked_posts', blank=True)
    date_created = models.DateTimeField()
    last_change = models.DateTimeField()

    def __str__(self):
        return f'{self.title} by {self.author.user.username}'


class Comment(models.Model):
    comment_content = models.TextField()
    date_written = models.DateTimeField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class BlockedUser(models.Model):
    user_blocker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocker_users")
    user_blocked = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocked_users")

    def __str__(self):
        return f'{self.user_blocker} blocked {self.user_blocked}'
