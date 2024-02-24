from flask import Flask, request, jsonify
from config import Config
from helpers import upload_file_to_s3
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return 'Ana Sayfa'

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Kullanıcıdan gelen ses dosyasını al
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    file_name = "user_audio.mp3"
    audio_file.save(file_name)

    # S3'e yükleme
    object_name = f"uploads/{file_name}"
    if not upload_file_to_s3(file_name, app.config['S3_BUCKET_NAME'], object_name):
        return jsonify({'error': 'Failed to upload audio file to S3'}), 500

    job_uri = f"s3://{app.config['S3_BUCKET_NAME']}/{object_name}"

    # Amazon Transcribe servisi için boto3 istemcisini oluştur
    try:
        transcribe = boto3.client('transcribe',
                                  aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                                  aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
                                  region_name=app.config['AWS_REGION_NAME'])
    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials are not configured properly.'}), 500

    # Transkripsiyon işini başlat
    job_name = "voice-to-text-job"
    language_code = "en-US"
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',
            LanguageCode=language_code,
        )
    except transcribe.exceptions.ClientError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Transcription started successfully. Please check later for results.'})

if __name__ == '__main__':
    app.run(debug=True)
