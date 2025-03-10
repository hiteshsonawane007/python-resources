# serializers.py

from rest_framework import serializers
from .models import S3File

class S3FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = S3File
        fields = '__all__'
