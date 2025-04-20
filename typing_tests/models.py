
from django.db import models

class TypingPassage(models.Model):
    title = models.CharField(max_length=100)
    order_id = models.IntegerField(default=1)
    passage_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    

   

    
