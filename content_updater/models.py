
from django.db import models
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
class news_bar(models.Model):
    news_bar_title=models.CharField(max_length=200, default='title here')
    news_bar_video_link=models.CharField(max_length=200, default='http://example.com')

    news_bar_order=models.IntegerField(default=0)

class our_videos(models.Model):
   
    our_videos_video_link=models.CharField(max_length=200, default='http://example.com')
    our_videos_order=models.IntegerField(default=0)




class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=[
        (1, '1 - Very Poor'),
        (2, '2 - Poor'), 
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ])
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} - {self.rating} stars"

    class Meta:
        ordering = ['-created_at']
