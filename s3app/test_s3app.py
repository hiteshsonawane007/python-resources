# test_s3app.py

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3
from rest_framework.test import APIClient  # Add this import

@pytest.fixture
def s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

@pytest.fixture
def client():
    return APIClient()  # Use Django REST framework test client

@pytest.mark.django_db
def test_upload_file(client, s3_client, monkeypatch):
    def mock_upload_fileobj(Fileobj, Bucket, Key):
        assert Bucket == settings.AWS_STORAGE_BUCKET_NAME
        assert Key == 'testfile.txt'
    
    monkeypatch.setattr(s3_client, 'upload_fileobj', mock_upload_fileobj)

    file = SimpleUploadedFile('testfile.txt', b'file_content')
    response = client.post('/s3app/upload/', {'file': file})

    print(response.json())  # Log response data for debugging

    assert response.status_code == 201
    assert response.json()['file_name'] == 'testfile.txt'
