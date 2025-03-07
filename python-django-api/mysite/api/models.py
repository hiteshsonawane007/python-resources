from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField()
    pusblished_date = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.title