from  .models import BlogPost
from rest_framework import serializers

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        #fields = '__all__'
        fields = ['id', 'title', 'content', 'pusblished_date']