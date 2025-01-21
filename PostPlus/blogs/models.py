from django.db import models
from django.contrib.auth.models import User


class blog(models.Model):
    TAG_CHOICES = [
        ('Personal blogs', 'Personal blogs'),
        ('Food', 'Food'),
        ('Education', 'Education'),
        ('History', 'History'),
        ('Corporate blogs', 'Corporate blogs'),
        ('Listicles', 'Listicles'),
        ('Infographics', 'Infographics'),
        ('Reviews', 'Reviews'),
        ('How-to guides', 'How-to guides'),
        ('Comparisons', 'Comparisons'),
        ('Vlogs', 'Vlogs'),
        ('Memes', 'Memes'),
        ('Affiliate blogs', 'Affiliate blogs'),
        ('Niche blogs', 'Niche blogs'),
        ('DIY blogs', 'DIY blogs'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200, default='Summary')
    content = models.TextField()
    tags= models.CharField(max_length=100, choices=TAG_CHOICES, default='Personal blogs')
    image = models.ImageField(upload_to='blog_images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

