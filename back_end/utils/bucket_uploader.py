import logging
import os

from flask import Flask, request
from google.cloud import storage

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

class BucketStorageClient:
    def __init__(self):
        self.gcs = storage.Client()
        self.bucket = self.gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    def upload_file(self, file):
        blob = self.bucket.blob("images/" + file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        blob.make_public()
        return blob.public_url