import logging
import os

from flask import Flask, request
from google.cloud import storage


class BucketStorageClient:
    def __init__(self):
        CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
        print(CLOUD_STORAGE_BUCKET)
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

class LocalStorageClient:
    def __init__(self, storage_location):
        self.storage_location = storage_location
    def upload_file(self, file):
        file.save(os.path.join(self.storage_location, file.filename))
        return "http://localhost:5000/static/"+file.filename

if __name__ == "__main__":
    BSC = BucketStorageClient()