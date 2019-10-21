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
        blob = self.bucket.blob(file.filename)
        blob.make_public()
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        return blob.public_url