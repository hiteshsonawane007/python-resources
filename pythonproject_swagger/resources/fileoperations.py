import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
import logging

from werkzeug.utils import secure_filename
from resources.ProgressPercentage import ProgressPercentage

blp = Blueprint("fileoperations", __name__, description="This is FileOperations REST APIs.")

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
session = boto3.Session(profile_name='AWSMorgan-136262601201')
s3_client = session.client('s3')
AWS_BUCKET_NAME = 'api-test-flask'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blp.route("/fileoperations/")
class FileOperations(MethodView):
    def post(self):
        try:
            file = request.files['file']

            if file.filename == '':
                abort(400, "No file selected for uploading.")
            if file and allowed_file(file.filename):
                config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                                        multipart_chunksize=1024 * 25, use_threads=True)
                s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file.filename)
                abort(201, "File successfully uploaded.")
            else:
                abort(400, "Allowed file types are txt, pdf, png, jpg, jpeg, gif")
        except ClientError as e:
            logging.error(e)
            abort(404, "Error In Execution")

    def delete(self):
        try:
            return "File Deleted!!"
        except:
            abort(404, "Error In Execution")
