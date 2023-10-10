import os
import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'eventopolis'
    location = 'media'


class StaticStorage(S3Boto3Storage):
    bucket_name = 'eventopolis'
    location = 'static'


def delete_image(image) -> None:
    if settings.DEBUG:
        os.remove(image.path)
    else:
        s3 = boto3.resource(
            's3', aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
        )
        s3.Object(
            MediaStorage.bucket_name,
            f'{MediaStorage.location}/{str(image)}'
        )