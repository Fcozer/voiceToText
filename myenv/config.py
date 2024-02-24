import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki değişkenleri yükler

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
