import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from config import Config

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """
    Dosyayı S3 bucket'ına yükler.
    """
    if object_name is None:
        object_name = file_name

    # S3 client oluştur
    s3_client = boto3.client('s3', aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                             region_name=Config.AWS_REGION_NAME)

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
